import shutil
import os

def copy_if_exists(src, dest, tracker=None):
    if src and os.path.exists(src):
        os.makedirs(dest, exist_ok=True)
        if os.path.isfile(src):
            if tracker:
                tracker.add_total(1)
                tracker.log_file(os.path.basename(src), src)
            try:
                shutil.copy2(src, dest)
                if tracker:
                    tracker.update(bytes_transferred=os.path.getsize(src))
            except Exception as e:
                if tracker:
                    tracker.add_error(f"Falha ao copiar arquivo {src}: {e}")
            return

        # Count all files first for accurate progress
        file_items = []
        for root, _, files in os.walk(src):
            rel_root = os.path.relpath(root, src)
            for f in files:
                total_path = os.path.join(root, f)
                rel_path = os.path.join(rel_root, f) if rel_root != '.' else f
                dest_path = os.path.join(dest, rel_path)
                file_items.append((f, total_path, dest_path))

        if tracker:
            tracker.add_total(len(file_items))

        for f, total_path, dest_path in file_items:
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            try:
                if tracker:
                    tracker.log_file(f, total_path, dest_path)
                shutil.copy2(total_path, dest_path)
                if tracker:
                    tracker.update(bytes_transferred=os.path.getsize(total_path))
            except Exception as e:
                if tracker:
                    tracker.add_error(f"Falha ao copiar {total_path}: {e}")
    else:
        if tracker:
            tracker.add_error(f"Caminho não encontrado: {src}")

def processar_local(job_config, base_local, tracker=None):
    apoio = job_config['vpn_apoio_root']
    copy_if_exists(os.path.join(apoio, "Lib"), f"{base_local}/Apoio/Lib", tracker=tracker)
    copy_if_exists(os.path.join(apoio, "Res"), f"{base_local}/Apoio/Res", tracker=tracker)

    copy_if_exists(job_config['vpn_originais'], f"{base_local}/Impressao/Originais", tracker=tracker)

    copy_if_exists(job_config['vpn_web_epub'], f"{base_local}/Web/ePub", tracker=tracker)
    copy_if_exists(job_config['vpn_metabooks'], f"{base_local}/Web/Metabooks", tracker=tracker)