import shutil
import os
import time

def copy_if_exists(src, dest):
    print(f"   [LOCAL] Iniciando cópia: {src} -> {dest}")
    if src and os.path.exists(src):
        os.makedirs(dest, exist_ok=True)
        # Se for um arquivo individual
        if os.path.isfile(src):
            try:
                shutil.copy2(src, dest)
                print(f"   [LOCAL] Copiado: {os.path.basename(src)}")
            except Exception as e:
                print(f"      [ERRO] Falha ao copiar arquivo {src}: {e}")
            return
        # Se for uma pasta: copiar arquivo a arquivo para dar feedback
        total = 0
        copied = 0
        # Conta aproximada de arquivos para feedback
        for _, _, files in os.walk(src):
            total += len(files)
        start = time.time()
        if total == 0:
            print(f"   [LOCAL] Pasta vazia: {src}")
        else:
            print(f"   [LOCAL] {total} arquivos para copiar...")
        for root, _, files in os.walk(src):
            rel_root = os.path.relpath(root, src)
            for f in files:
                total_path = os.path.join(root, f)
                rel_path = os.path.join(rel_root, f) if rel_root != '.' else f
                dest_path = os.path.join(dest, rel_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                try:
                    # Feedback por arquivo
                    print(f"   [LOCAL] Copiando: {rel_path}")
                    shutil.copy2(total_path, dest_path)
                    copied += 1
                    # Feedback periódico também mantido
                    if copied % 50 == 0 or copied == total:
                        elapsed = int(time.time() - start)
                        print(f"   [LOCAL] Copiados {copied}/{total} arquivos - {elapsed}s")
                except Exception as e:
                    print(f"      [ERRO] Falha ao copiar {total_path}: {e}")
        print(f"   [LOCAL] Concluído: {copied} arquivos copiados de {src}")
    else:
        print(f"   [AVISO] Caminho não encontrado: {src}")

def processar_local(job_config, base_local):
    print("-> Iniciando coleta de arquivos locais (VPN/OneDrive)...")

    # 1. Apoio (Busca Lib e Res dentro da raiz de apoio)
    apoio = job_config['vpn_apoio_root']
    print(f"   [LOCAL] Tentando: {os.path.join(apoio, 'Lib')} -> {base_local}/Apoio/Lib")
    copy_if_exists(os.path.join(apoio, "Lib"), f"{base_local}/Apoio/Lib")
    print(f"   [LOCAL] Tentando: {os.path.join(apoio, 'Res')} -> {base_local}/Apoio/Res")
    copy_if_exists(os.path.join(apoio, "Res"), f"{base_local}/Apoio/Res")

    # 2. Originais (Caminho direto)
    print(f"   [LOCAL] Tentando: {job_config['vpn_originais']} -> {base_local}/Impressao/Originais")
    copy_if_exists(job_config['vpn_originais'], f"{base_local}/Impressao/Originais")

    # 3. Web (ePub e Metabooks caminhos diretos)
    print(f"   [LOCAL] Tentando: {job_config['vpn_web_epub']} -> {base_local}/Web/ePub")
    copy_if_exists(job_config['vpn_web_epub'], f"{base_local}/Web/ePub")
    print(f"   [LOCAL] Tentando: {job_config['vpn_metabooks']} -> {base_local}/Web/Metabooks")
    copy_if_exists(job_config['vpn_metabooks'], f"{base_local}/Web/Metabooks")