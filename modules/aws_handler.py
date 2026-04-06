import os
import json
from urllib.parse import urlparse
import boto3
from botocore.exceptions import ClientError, ProfileNotFound, NoCredentialsError
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from datetime import datetime

def parse_s3_uri(s3_uri):
    p = urlparse(s3_uri)
    bucket = p.netloc
    prefix = p.path.lstrip('/')
    return bucket, prefix


def _ensure_local_dir(path):
    os.makedirs(path, exist_ok=True)


def sync_s3_to_local(s3_uri, local_root, session=None, max_workers=8):
    session = session or boto3.Session()
    s3 = session.client('s3')
    bucket, prefix = parse_s3_uri(s3_uri)
    paginator = s3.get_paginator('list_objects_v2')

    _ensure_local_dir(local_root)

    keys = []
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get('Contents', []):
            key = obj['Key']
            if key.endswith('/'):
                continue
            keys.append(key)

    if not keys:
        print(f"   [AWS SYNC] Nenhum objeto encontrado em {s3_uri}")
        # Debug: listar alguns objetos próximos ao prefix para ajudar a identificar o problema
        try:
            # tenta listar na raiz do prefix (um nível acima) para detectar pastas similares
            parent = '/'.join(prefix.rstrip('/').split('/')[:-1])
            parent = parent.rstrip('/') + '/' if parent else ''
            print(f"   [AWS SYNC] Tentando listar objetos próximos ao prefix: s3://{bucket}/{parent} (debug)")
            debug_keys = []
            count = 0
            for page in s3.get_paginator('list_objects_v2').paginate(Bucket=bucket, Prefix=parent):
                for obj in page.get('Contents', []):
                    k = obj['Key']
                    print(f"      [DBG] {k}")
                    debug_keys.append(k)
                    count += 1
                    if count >= 200:
                        break
                if count >= 200:
                    break

            if not debug_keys:
                print("      [DBG] Nenhum objeto encontrado no nível de debug também.")
                return

            # Se foram encontrados objetos próximos, tentar usar esses objetos como fallback.
            # Determinar o prefixo comum em termos de diretório (não char-wise).
            def _common_s3_dir_prefix(keys_list):
                parts = [k.split('/') for k in keys_list]
                common = []
                for idx in range(min(len(p) for p in parts)):
                    seg = parts[0][idx]
                    if all(p[idx] == seg for p in parts):
                        common.append(seg)
                    else:
                        break
                if not common:
                    return ''
                return '/'.join(common) + '/'

            base_prefix = _common_s3_dir_prefix(debug_keys)
            if base_prefix:
                print(f"   [AWS SYNC] Usando fallback com prefix comum detectado: s3://{bucket}/{base_prefix}")
                # substituir keys pela lista encontrada e ajustar prefix para cálculo de paths locais
                keys = [k for k in debug_keys if not k.endswith('/')]
                prefix = base_prefix
            else:
                # se não for possível determinar prefixo comum confiável, abortar para evitar downloads errados
                print("   [AWS SYNC] Não foi possível determinar um prefixo comum para fallback. Abortando.")
                return
        except Exception as e:
            print(f"   [AWS SYNC] Erro ao listar para debug: {e}")
            return

    def _download(key):
        # Garantir que o caminho local seja relativo ao prefix correto.
        # Evita situações onde os.path.relpath produz caminhos com '..' quando
        # key não está abaixo de prefix (isso causava criação de pastas Abertos/Fechados
        # dentro de Originais, por exemplo).
        if prefix and key.startswith(prefix):
            rel_path = key[len(prefix):].lstrip('/')
        else:
            # fallback: usar apenas o nome do arquivo para evitar diretórios indesejados
            rel_path = os.path.basename(key)
        # normalizar separadores para o filesystem local
        rel_path = rel_path.replace('/', os.sep)
        local_path = os.path.join(local_root, rel_path)
        _ensure_local_dir(os.path.dirname(local_path))
        try:
            s3.download_file(bucket, key, local_path)
            return (key, True, None)
        except ClientError as e:
            return (key, False, str(e))

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(_download, k): k for k in keys}
        for fut in as_completed(futures):
            key = futures[fut]
            ok = False
            try:
                _, ok, err = fut.result()
            except Exception as e:
                ok = False
                err = str(e)
            if not ok:
                print(f"      [ERRO] Falha ao baixar {key}: {err}")


def sync_local_to_s3(local_root, s3_uri, session=None, max_workers=8):
    session = session or boto3.Session()
    s3 = session.client('s3')
    bucket, prefix = parse_s3_uri(s3_uri)

    if not os.path.exists(local_root):
        print(f"   [AWS SYNC] Pasta local não existe: {local_root}")
        return

    uploads = []
    for root, _, files in os.walk(local_root):
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, local_root)
            key = os.path.join(prefix, rel).replace('\\', '/')
            uploads.append((full, key))

    def _upload(item):
        full, key = item
        # Progresso por arquivo
        print(f"   [AWS UPLOAD] Enviando: {full} -> s3://{bucket}/{key}")
        try:
            s3.upload_file(full, bucket, key)
            print(f"   [AWS UPLOAD] Enviado: {full} -> s3://{bucket}/{key}")
            return (key, True, None, full)
        except Exception as e:
            print(f"   [AWS UPLOAD] ERRO ao enviar {full}: {e}")
            # Captura qualquer erro de upload e retorna para não elevar exceção no executor
            return (key, False, str(e), full)
        finally:
            # Atualiza contador de progresso global e imprime resumo parcial
            try:
                with lock:
                    counter['done'] += 1
                    done = counter['done']
                print(f"   [AWS UPLOAD] Progresso: {done}/{total}")
            except Exception:
                pass

    # listas para logs
    success_list = []
    fail_list = []
    lock = Lock()

    total = len(uploads)
    counter = {'done': 0}
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
                        print(f"      [ERRO] Falha ao subir {key}: {err}")
            except Exception as e:
                print(f"      [ERRO] Exceção inesperada durante upload: {e}")

    # Escrever logs no diretório local_root
    try:
        logs_dir = os.path.join(local_root, 'upload_logs')
        os.makedirs(logs_dir, exist_ok=True)
        success_path = os.path.join(logs_dir, 'upload_success.json')
        failed_path = os.path.join(logs_dir, 'upload_failed.json')
        with open(success_path, 'w', encoding='utf-8') as f:
            json.dump(success_list, f, ensure_ascii=False, indent=2)
        with open(failed_path, 'w', encoding='utf-8') as f:
            json.dump(fail_list, f, ensure_ascii=False, indent=2)
        print(f"   [AWS UPLOAD] Logs gravados: {success_path} ({len(success_list)}), {failed_path} ({len(fail_list)})")
        # Também copia logs para o diretório global reports/ com timestamp
        try:
            reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'reports'))
            os.makedirs(reports_dir, exist_ok=True)
            ts = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            rep_success = os.path.join(reports_dir, f'upload_success_{ts}.json')
            rep_failed = os.path.join(reports_dir, f'upload_failed_{ts}.json')
            with open(rep_success, 'w', encoding='utf-8') as f:
                json.dump(success_list, f, ensure_ascii=False, indent=2)
            with open(rep_failed, 'w', encoding='utf-8') as f:
                json.dump(fail_list, f, ensure_ascii=False, indent=2)
            print(f"   [AWS UPLOAD] Logs copiados para reports/: {rep_success}, {rep_failed}")
        except Exception as e:
            print(f"   [AWS UPLOAD] Erro ao copiar logs para reports/: {e}")
    except Exception as e:
        print(f"   [AWS UPLOAD] Erro ao gravar logs de upload: {e}")


def _create_session_with_fallback(profile="publishing"):
    try:
        session = boto3.Session(profile_name=profile) if profile else boto3.Session()
    except ProfileNotFound:
        print(f'   [AWS SYNC] Perfil AWS "{profile}" não encontrado. Usando credenciais padrão/variáveis de ambiente.')
        session = boto3.Session()

    # Se sessão não tiver credenciais, tentar carregar de config/credentials.json
    try:
        creds = session.get_credentials()
        has_creds = bool(creds and creds.access_key)
    except Exception:
        has_creds = False

    if not has_creds:
        cred_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config', 'credentials.json'))
        if os.path.exists(cred_path):
            try:
                with open(cred_path, 'r', encoding='utf-8') as f:
                    c = json.load(f)
                access = c.get('aws_access_key') or c.get('aws_access_key_id')
                secret = c.get('aws_secret_key') or c.get('aws_secret_access_key')
                if access and secret:
                    session = boto3.Session(aws_access_key_id=access, aws_secret_access_key=secret)
                    print('   [AWS SYNC] Usando credenciais do arquivo config/credentials.json')
                else:
                    print('   [AWS SYNC] Arquivo config/credentials.json encontrado, mas chaves não estão no formato esperado.')
            except Exception as e:
                print(f'   [AWS SYNC] Erro ao ler credenciais locais: {e}')
        else:
            print('   [AWS SYNC] Nenhuma credencial AWS encontrada (perfil, variáveis de ambiente ou config/credentials.json).')

    return session


def _list_immediate_prefixes(session, bucket, prefix):
    s3 = session.client('s3')
    prefixes = []
    try:
        paginator = s3.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix.rstrip('/') + '/', Delimiter='/'):
            for cp in page.get('CommonPrefixes', []):
                prefixes.append(cp['Prefix'])
    except Exception as e:
        print(f"   [AWS SYNC] Erro ao listar prefixes para debug: {e}")
    return prefixes


def run_s3_sync(source, dest, profile="publishing"):
    """
    Motor principal de transferência.
    Agora usa boto3 internamente para S3<->Local. Mantém API compatível.
    """
    if not (source and dest):
        return

    source = source.rstrip('/') + '/'
    print(f"   [AWS SYNC] Sincronizando: {source} -> {dest}")

    # Decide direção pelo prefix "s3://"
    session = _create_session_with_fallback(profile)

    if source.startswith('s3://') and not dest.startswith('s3://'):
        # S3 -> Local
        try:
            sync_s3_to_local(source, dest, session=session)
        except NoCredentialsError:
            print('   [AWS SYNC] Erro: credenciais AWS não encontradas. Configure um profile, variáveis de ambiente, ou coloque chaves em config/credentials.json')
    elif dest.startswith('s3://') and not source.startswith('s3://'):
        # Local -> S3
        try:
            # Verifica se o bucket de destino existe antes de iniciar uploads
            s3_check = session.client('s3')
            b_dst, _ = parse_s3_uri(dest)
            try:
                s3_check.head_bucket(Bucket=b_dst)
            except Exception as e:
                print(f"   [AWS SYNC] Erro: bucket de destino 's3://{b_dst}' não encontrado ou inacessível: {e}")
                print("   -> Verifique o nome do bucket ou suas permissões e tente novamente.")
                return
            sync_local_to_s3(source, dest, session=session)
        except NoCredentialsError:
            print('   [AWS SYNC] Erro: credenciais AWS não encontradas. Configure um profile, variáveis de ambiente, ou coloque chaves em config/credentials.json')
    else:
        # s3:// para s3:// (copiar dentro do S3) ou local->local (fallback para aws cli era mais rápido)
        if source.startswith('s3://') and dest.startswith('s3://'):
            # copia dentro do S3: listar objetos e copiar via copy_object
            s3 = session.client('s3')
            b_src, p_src = parse_s3_uri(source)
            b_dst, p_dst = parse_s3_uri(dest)
            paginator = s3.get_paginator('list_objects_v2')
            for page in paginator.paginate(Bucket=b_src, Prefix=p_src):
                for obj in page.get('Contents', []):
                    key = obj['Key']
                    if key.endswith('/'):
                        continue
                    rel = os.path.relpath(key, p_src)
                    dst_key = os.path.join(p_dst, rel).replace('\\', '/')
                    copy_source = {'Bucket': b_src, 'Key': key}
                    try:
                        s3.copy(copy_source, b_dst, dst_key)
                    except ClientError as e:
                        print(f"      [ERRO] Falha ao copiar {key}: {e}")
        else:
            # local -> local: apenas cria a pasta de destino e copia arquivos
            if os.path.isdir(source):
                _ensure_local_dir(dest)
                for root, _, files in os.walk(source):
                    for f in files:
                        srcf = os.path.join(root, f)
                        rel = os.path.relpath(srcf, source)
                        dstf = os.path.join(dest, rel)
                        _ensure_local_dir(os.path.dirname(dstf))
                        try:
                            with open(srcf, 'rb') as r, open(dstf, 'wb') as w:
                                w.write(r.read())
                        except Exception as e:
                            print(f"      [ERRO] Falha ao copiar {srcf} -> {dstf}: {e}")


def processar_aws(job_config, base_local):
    """
    Lógica de INPUT: Coleta Capa e Miolo das raízes fornecidas.
    Substitui o antigo 'run_download'.
    """
    print("\n[MÓDULO AWS] Iniciando coleta de materiais (Capa/Miolo)...")

    # Processamento de Capa
    capa_root = job_config['s3_capa_root'].rstrip('/')
    # Detectar subpastas (Aberto/Fechado) dinamicamente
    session = _create_session_with_fallback()
    bucket, root_prefix = parse_s3_uri(capa_root)
    prefixes = _list_immediate_prefixes(session, bucket, root_prefix)
    if prefixes:
        # para cada prefix encontrado, decidir destino local
        for p in prefixes:
            name = os.path.basename(p.rstrip('/'))
            if 'aberto' in name.lower():
                run_s3_sync(f"s3://{bucket}/{p}", f"{base_local}/Impressao/Abertos/Capa")
            elif 'fechado' in name.lower() or 'closed' in name.lower():
                run_s3_sync(f"s3://{bucket}/{p}", f"{base_local}/Impressao/Fechados/Capa")
            else:
                # não reconhecido: baixar para uma pasta genérica de Apoio/Capa
                run_s3_sync(f"s3://{bucket}/{p}", f"{base_local}/Impressao/Apoio/Capa")
    else:
        # fallback: baixar todo o conteúdo da raiz
        run_s3_sync(f"{capa_root}", f"{base_local}/Impressao/Abertos/Capa")

    # Processamento de Miolo
    miolo_root = job_config['s3_miolo_root'].rstrip('/')
    run_s3_sync(f"{miolo_root}/Impressao/Abertos/Miolo", f"{base_local}/Impressao/Abertos/Miolo")
    run_s3_sync(f"{miolo_root}/Impressao/Fechados/Miolo", f"{base_local}/Impressao/Fechados/Miolo")
    run_s3_sync(f"{miolo_root}/Impressao/Original", f"{base_local}/Impressao/Originais")


def upload_final(base_local, s3_destino):
    """
    Lógica de OUTPUT: Sobe toda a estrutura organizada para o S3.
    Substitui o antigo 'upload_pasta'.
    """
    print("\n[MÓDULO AWS] Iniciando armazenamento final no S3...")
    run_s3_sync(base_local, s3_destino)