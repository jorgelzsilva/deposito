import os
import json
from urllib.parse import urlparse
import boto3
from botocore.exceptions import ClientError, ProfileNotFound, NoCredentialsError
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from datetime import datetime
import time
import shutil
from botocore.config import Config

def _safe_win_path(path):
    if os.name == 'nt' and not path.startswith('\\\\?\\'):
        path = os.path.abspath(path)
        if path.startswith('\\\\'):
            return '\\\\?\\UNC\\' + path[2:]
        return '\\\\?\\' + path
    return path

def _get_s3_client(session):
    return session.client('s3', config=Config(retries={'max_attempts': 10, 'mode': 'standard'}, max_pool_connections=20))

class TransferCallback(object):
    def __init__(self, target_size, filename):
        self._target_size = target_size
        self._filename = filename
        self._seen_so_far = 0
        self._lock = Lock()
        self._start_time = time.time()
        self._last_print_time = self._start_time

    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount

def parse_s3_uri(s3_uri):
    p = urlparse(s3_uri)
    bucket = p.netloc
    prefix = p.path.lstrip('/')
    return bucket, prefix


def _ensure_local_dir(path):
    os.makedirs(_safe_win_path(path), exist_ok=True)


def sync_s3_to_local(s3_uri, local_root, session=None, max_workers=8, tracker=None):
    session = session or boto3.Session()
    s3 = _get_s3_client(session)
    bucket, prefix = parse_s3_uri(s3_uri)
    paginator = s3.get_paginator('list_objects_v2')

    _ensure_local_dir(local_root)

    keys = []
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get('Contents', []):
            key = obj['Key']
            if key.endswith('/'):
                continue
            keys.append((key, obj.get('Size', 0)))

    if not keys:
        return

    if tracker:
        tracker.add_total(len(keys))

    def _download(item):
        key, file_size = item
        if prefix and key.startswith(prefix):
            rel_path = key[len(prefix):].lstrip('/')
        else:
            rel_path = os.path.basename(key)
        rel_path = rel_path.replace('/', os.sep)
        local_path = os.path.join(local_root, rel_path)
        _ensure_local_dir(os.path.dirname(local_path))
        try:
            if tracker:
                tracker.log_file(os.path.basename(key), f"s3://{bucket}/{key}")
            s3.download_file(bucket, key, local_path)
            if tracker:
                tracker.update(bytes_transferred=file_size)
            return (key, True, None)
        except ClientError as e:
            if tracker:
                tracker.add_error(f"Falha ao baixar {key}: {e}")
            return (key, False, str(e))

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(_download, k): k[0] for k in keys}
        for fut in as_completed(futures):
            try:
                _, ok, err = fut.result()
            except Exception as e:
                if tracker:
                    tracker.add_error(f"Erro inesperado ao baixar: {e}")


def sync_local_to_s3(local_root, s3_uri, session=None, max_workers=8, tracker=None):
    session = session or boto3.Session()
    s3 = _get_s3_client(session)
    bucket, prefix = parse_s3_uri(s3_uri)

    if not os.path.exists(local_root):
        return

    uploads = []
    for root, _, files in os.walk(local_root):
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, local_root)
            key = os.path.join(prefix, rel).replace('\\', '/')
            target_size = os.path.getsize(full)
            uploads.append((full, key, target_size))

    if tracker:
        tracker.add_total(len(uploads))

    def _upload(item):
        full, key, file_size = item
        try:
            if tracker:
                tracker.log_file(os.path.basename(full), full, f"s3://{bucket}/{key}")
            s3.upload_file(full, bucket, key)
            if tracker:
                tracker.update(bytes_transferred=file_size)
            return (key, True, None, full)
        except Exception as e:
            if tracker:
                tracker.add_error(f"Falha ao subir {key}: {e}")
            return (key, False, str(e), full)

    success_list = []
    fail_list = []
    lock = Lock()

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(_upload, u): u for u in uploads}
        for fut in as_completed(futures):
            try:
                key, ok, err, full = fut.result()
                if ok:
                    with lock:
                        success_list.append({'file': full, 's3_key': key})
                else:
                    with lock:
                        fail_list.append({'file': full, 's3_key': key, 'error': err})
            except Exception as e:
                if tracker:
                    tracker.add_error(f"Exceção durante upload: {e}")

    try:
        logs_dir = os.path.join(local_root, 'upload_logs')
        os.makedirs(logs_dir, exist_ok=True)
        success_path = os.path.join(logs_dir, 'upload_success.json')
        failed_path = os.path.join(logs_dir, 'upload_failed.json')
        with open(success_path, 'w', encoding='utf-8') as f:
            json.dump(success_list, f, ensure_ascii=False, indent=2)
        with open(failed_path, 'w', encoding='utf-8') as f:
            json.dump(fail_list, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def _create_session_with_fallback(profile=None):
    cred_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config', 'credentials.json'))
    if os.path.exists(cred_path):
        try:
            with open(cred_path, 'r', encoding='utf-8') as f:
                c = json.load(f)
            access = c.get('aws_access_key') or c.get('aws_access_key_id')
            secret = c.get('aws_secret_key') or c.get('aws_secret_access_key')
            if access and secret:
                return boto3.Session(aws_access_key_id=access, aws_secret_access_key=secret)
        except Exception:
            pass
    return boto3.Session()


def _list_immediate_prefixes(session, bucket, prefix):
    s3 = _get_s3_client(session)
    prefixes = []
    try:
        paginator = s3.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix.rstrip('/') + '/', Delimiter='/'):
            for cp in page.get('CommonPrefixes', []):
                prefixes.append(cp['Prefix'])
    except Exception:
        pass
    return prefixes


def run_s3_sync(source, dest, profile="publishing", tracker=None):
    """
    Motor principal de transferência.
    Agora usa boto3 internamente para S3<->Local. Mantém API compatível.
    """
    if not (source and dest):
        return

    source = source.rstrip('/') + '/'

    session = _create_session_with_fallback(profile) if source.startswith('s3://') or dest.startswith('s3://') else None

    if source.startswith('s3://') and not dest.startswith('s3://'):
        try:
            sync_s3_to_local(source, dest, session=session, tracker=tracker)
        except NoCredentialsError:
            if tracker:
                tracker.add_error("Credenciais AWS não encontradas")
    elif dest.startswith('s3://') and not source.startswith('s3://'):
        try:
            s3_check = _get_s3_client(session)
            b_dst, _ = parse_s3_uri(dest)
            try:
                s3_check.head_bucket(Bucket=b_dst)
            except Exception as e:
                if tracker:
                    tracker.add_error(f"Bucket de destino não encontrado ou inacessível: {e}")
                return
            sync_local_to_s3(source, dest, session=session, tracker=tracker)
        except NoCredentialsError:
            if tracker:
                tracker.add_error("Credenciais AWS não encontradas")
    else:
        if source.startswith('s3://') and dest.startswith('s3://'):
            s3 = _get_s3_client(session)
            b_src, p_src = parse_s3_uri(source)
            b_dst, p_dst = parse_s3_uri(dest)
            paginator = s3.get_paginator('list_objects_v2')
            # Collect all keys first for accurate count
            copy_items = []
            for page in paginator.paginate(Bucket=b_src, Prefix=p_src):
                for obj in page.get('Contents', []):
                    key = obj['Key']
                    if key.endswith('/'):
                        continue
                    rel = os.path.relpath(key, p_src)
                    dst_key = os.path.join(p_dst, rel).replace('\\', '/')
                    copy_items.append((key, dst_key, obj.get('Size', 0)))
            if tracker and copy_items:
                tracker.add_total(len(copy_items))
            for key, dst_key, size in copy_items:
                copy_source = {'Bucket': b_src, 'Key': key}
                try:
                    if tracker:
                        tracker.log_file(os.path.basename(key), f"s3://{b_src}/{key}", f"s3://{b_dst}/{dst_key}")
                    s3.copy(copy_source, b_dst, dst_key)
                    if tracker:
                        tracker.update(bytes_transferred=size)
                except ClientError as e:
                    if tracker:
                        tracker.add_error(f"Falha ao copiar {key}: {e}")
        else:
            if os.path.isdir(source):
                _ensure_local_dir(dest)
                # Collect all files first for accurate count
                file_items = []
                for root, _, files in os.walk(source):
                    for f in files:
                        srcf = os.path.join(root, f)
                        rel = os.path.relpath(srcf, source)
                        dstf = os.path.join(dest, rel)
                        file_items.append((f, srcf, dstf))
                if tracker and file_items:
                    tracker.add_total(len(file_items))
                for f, srcf, dstf in file_items:
                    _ensure_local_dir(os.path.dirname(dstf))
                    try:
                        src_safe = _safe_win_path(srcf)
                        dst_safe = _safe_win_path(dstf)
                        if tracker:
                            tracker.log_file(f, srcf, dstf)
                        shutil.copy2(src_safe, dst_safe)
                        if tracker:
                            tracker.update(bytes_transferred=os.path.getsize(src_safe))
                    except Exception as e:
                        if tracker:
                            tracker.add_error(f"Falha ao copiar {srcf}: {e}")


def _sync_originais(session, miolo_root, local_dest, tracker=None):
    s3 = _get_s3_client(session)
    candidatos = ["Originais", "Original"]
    bucket, _ = parse_s3_uri(miolo_root)

    for nome in candidatos:
        uri = f"{miolo_root}/Impressao/{nome}"
        _, prefix = parse_s3_uri(uri + '/')
        resp = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, MaxKeys=1)
        if resp.get('Contents'):
            run_s3_sync(uri, local_dest, tracker=tracker)
            return

    if tracker:
        tracker.add_error("Nenhuma pasta de Originais/Original encontrada no S3.")


def processar_aws(job_config, base_local, tracker=None):
    capa_root = job_config.get('s3_capa_root', '').rstrip('/').strip()
    if capa_root.startswith('s3://'):
        session = _create_session_with_fallback()
        bucket, root_prefix = parse_s3_uri(capa_root)
        prefixes = _list_immediate_prefixes(session, bucket, root_prefix)
        if prefixes:
            for p in prefixes:
                name = os.path.basename(p.rstrip('/'))
                if 'aberto' in name.lower():
                    run_s3_sync(f"s3://{bucket}/{p}", f"{base_local}/Impressao/Abertos/Capa", tracker=tracker)
                elif 'fechado' in name.lower() or 'closed' in name.lower():
                    run_s3_sync(f"s3://{bucket}/{p}", f"{base_local}/Impressao/Fechados/Capa", tracker=tracker)
                else:
                    run_s3_sync(f"s3://{bucket}/{p}", f"{base_local}/Impressao/Apoio/Capa", tracker=tracker)
        else:
            run_s3_sync(f"{capa_root}", f"{base_local}/Impressao/Abertos/Capa", tracker=tracker)
    elif capa_root:
        if os.path.isdir(capa_root):
            subdirs = [os.path.join(capa_root, d) for d in os.listdir(capa_root) if os.path.isdir(os.path.join(capa_root, d))]
            if subdirs:
                for d in subdirs:
                    name = os.path.basename(d)
                    if 'aberto' in name.lower():
                        run_s3_sync(d, f"{base_local}/Impressao/Abertos/Capa", tracker=tracker)
                    elif 'fechado' in name.lower() or 'closed' in name.lower():
                        run_s3_sync(d, f"{base_local}/Impressao/Fechados/Capa", tracker=tracker)
                    else:
                        run_s3_sync(d, f"{base_local}/Impressao/Apoio/Capa", tracker=tracker)
            else:
                run_s3_sync(capa_root, f"{base_local}/Impressao/Abertos/Capa", tracker=tracker)
        else:
            if tracker:
                tracker.add_error(f"Diretório local de capa não encontrado: {capa_root}")

    # Processamento de Miolo
    miolo_root = job_config.get('s3_miolo_root', '').rstrip('/').strip()
    if miolo_root.startswith('s3://'):
        session = _create_session_with_fallback()
        run_s3_sync(f"{miolo_root}/Impressao/Abertos/Miolo", f"{base_local}/Impressao/Abertos/Miolo", tracker=tracker)
        run_s3_sync(f"{miolo_root}/Impressao/Fechados/Miolo", f"{base_local}/Impressao/Fechados/Miolo", tracker=tracker)
        _sync_originais(session, miolo_root, f"{base_local}/Impressao/Originais", tracker=tracker)
    elif miolo_root:
        if os.path.isdir(miolo_root):
            run_s3_sync(os.path.join(miolo_root, "Impressao", "Abertos", "Miolo"), f"{base_local}/Impressao/Abertos/Miolo", tracker=tracker)
            run_s3_sync(os.path.join(miolo_root, "Impressao", "Fechados", "Miolo"), f"{base_local}/Impressao/Fechados/Miolo", tracker=tracker)
            candidatos = ["Originais", "Original"]
            encontrado = False
            for nome in candidatos:
                caminho = os.path.join(miolo_root, "Impressao", nome)
                if os.path.isdir(caminho):
                    run_s3_sync(caminho, f"{base_local}/Impressao/Originais", tracker=tracker)
                    encontrado = True
                    break
            if not encontrado:
                if tracker:
                    tracker.add_error("Nenhuma pasta de Originais/Original encontrada localmente.")
        else:
            if tracker:
                tracker.add_error(f"Diretório local de miolo não encontrado: {miolo_root}")


def upload_final(base_local, s3_destino, tracker=None):
    run_s3_sync(base_local, s3_destino, tracker=tracker)