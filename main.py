import os
import sys
import re
from config import settings
from modules import aws_handler, vpn_handler, indesign_parser, ai_agent, sync_manager
from modules.progress_tracker import ProgressTracker

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')

    job = settings.JOB
    try:
        settings_file = os.path.join(os.path.dirname(__file__), 'config', 'settings.py')
        with open(settings_file, 'r', encoding='utf-8', errors='replace') as f:
            src = f.read()
        ns = {}
        exec(compile(src, settings_file, 'exec'), ns)
        if 'JOB' in ns and isinstance(ns['JOB'], dict):
            job = ns['JOB']
    except Exception:
        pass

    base_local = os.path.abspath(os.path.join(settings.PATHS['temp_local'], job['nome_projeto']))

    print("="*60)
    print(f" INICIANDO AUTOMAÇÃO: {job['nome_projeto']}")
    print("="*60)

    sync_manager.setup_estrutura(base_local)

    tracker = ProgressTracker()
    tracker.start_phase(0, 0)

    if settings.MODULOS['aws_input']:
        aws_handler.processar_aws(job, base_local, tracker=tracker)

    if settings.MODULOS['vpn_sync']:
        vpn_handler.processar_local(job, base_local, tracker=tracker)

    if settings.MODULOS['indesign_parser']:
        caminho_miolo = os.path.join(base_local, "Impressao/Abertos/Miolo")
        links_necessarios = indesign_parser.run(caminho_miolo)

        COMMON_EXT = r'(?:eps|jpg|jpeg|tif|tiff|png|pdf|zip|xml|psd|otf|ttf|ai|svg|bmp)'
        FNAME_RE = re.compile(r'([^\\/:]+\.' + COMMON_EXT + r')', re.IGNORECASE)

        def clean_name(n):
            if not n:
                return None
            n = str(n).strip()
            m = FNAME_RE.search(n)
            if m:
                return m.group(1).strip()
            s = ''.join(ch for ch in n if ch.isprintable())
            s = re.sub(r'\s+', ' ', s).strip()
            return s if s else None

        links_unicos = sorted({clean_name(l) for l in links_necessarios if clean_name(l)})
        links_path = os.path.join(base_local, "links_extracted.txt")
        with open(links_path, 'w', encoding='utf-8') as f:
            for l in links_unicos:
                f.write(l + '\n')

        arquivos_locais = []
        if os.path.exists(caminho_miolo):
            for root, _, files in os.walk(caminho_miolo):
                for fn in files:
                    arquivos_locais.append(fn)
        arquivos_locais_unicos = sorted({a for a in arquivos_locais if a})
        arquivos_path = os.path.join(base_local, "files_local_miolo.txt")
        with open(arquivos_path, 'w', encoding='utf-8') as f:
            for a in arquivos_locais_unicos:
                f.write(a + '\n')

        faltantes = sorted(list(set(links_unicos) - set(arquivos_locais_unicos)))
        faltantes_path = os.path.join(base_local, "faltantes_links.txt")
        with open(faltantes_path, 'w', encoding='utf-8') as f:
            for it in faltantes:
                f.write(it + '\n')

        verificacao = []
        for falt in faltantes:
            matches = []
            for root, _, files in os.walk(base_local):
                for fn in files:
                    try:
                        if fn.lower() == falt.lower() or fn.lower().endswith(falt.lower()):
                            matches.append(os.path.join(root, fn))
                    except Exception:
                        continue
            verificacao.append((falt, matches))

        verificacao_path = os.path.join(base_local, "faltantes_verificados.txt")
        found_count = 0
        with open(verificacao_path, 'w', encoding='utf-8') as f:
            for falt, matches in verificacao:
                if matches:
                    found_count += 1
                    f.write(f"FOUND\t{falt}\t" + ";".join(matches) + "\n")
                else:
                    f.write(f"MISSING\t{falt}\n")
                    tracker.add_missing_file(falt)

        if faltantes and settings.MODULOS['ai_agent']:
            print(f"\n--- [!] {len(faltantes)} links ausentes detectados ---")
            print("--- Consultando IA para buscar nos Originais... ---")

            pasta_originais = os.path.join(base_local, "Impressao/Originais")
            arquivos_originais = os.listdir(pasta_originais) if os.path.exists(pasta_originais) else []

            sugestoes = ai_agent.run(faltantes, arquivos_originais, settings.PATHS['lm_studio_url'], output_dir=base_local)
            print("-> Relatório de sugestões da IA gerado na raiz do projeto.")

    phase1_data = tracker.finish_phase()

    if settings.MODULOS['aws_output']:
        print("\n--- Preparado para subir estrutura consolidada para AWS S3 Final ---")
        try:
            s3_final_raw = job.get('s3_final_root', '')
            s3_final = str(s3_final_raw).strip() if s3_final_raw is not None else ''
            if not s3_final:
                settings_file = os.path.join(os.path.dirname(__file__), 'config', 'settings.py')
                with open(settings_file, 'r', encoding='utf-8', errors='replace') as f:
                    txt = f.read()
                m = re.search(r'"s3_final_root"\s*:\s*"([^"]*)"', txt)
                if m:
                    s3_final = m.group(1).strip()
        except Exception:
            s3_final = ''
        s3_final_raw = settings.JOB.get('s3_final_root', '')
        try:
            s3_final = str(s3_final_raw).strip()
        except Exception:
            s3_final = ''
        if not s3_final:
            print("-> AVISO: JOB['s3_final_root'] não está configurado em config/settings.py. Upload final será ignorado.")
            destino_s3 = None
        else:
            destino_s3 = s3_final.rstrip('/') + f"/{job['nome_projeto']}/"

        if not destino_s3:
            print("-> Upload final PULADO: destino S3 não configurado.")
        else:
            upload_ok_file = os.path.join(base_local, "UPLOAD_OK")
            auto = os.environ.get('AUTO_UPLOAD') == '1' or os.path.exists(upload_ok_file)
            if not auto:
                print("-> Upload pausado aguardando sinal verde.")
                print("   Crie o arquivo 'UPLOAD_OK' na pasta do projeto ou defina a variável de ambiente AUTO_UPLOAD=1 para subir automaticamente.")
                print("-> Pressione 's' e Enter para subir agora, ou qualquer outra tecla para pular:")
                resp = input().strip().lower()
                if resp != 's':
                    print("-> Upload final PULADO pelo usuário.")
                else:
                    print("-> Sinal verde recebido. Iniciando upload...")
                    tracker.start_phase(1, 0)
                    aws_handler.upload_final(base_local, destino_s3, tracker=tracker)
                    tracker.finish_phase()
            else:
                print("-> Modo automático: iniciando upload...")
                tracker.start_phase(1, 0)
                aws_handler.upload_final(base_local, destino_s3, tracker=tracker)
                tracker.finish_phase()

    print("\n--- Gerando Resumo de Arquivos (tree) ---")
    relatorio_txt = os.path.join(base_local, "arquivos.txt")
    os.system(f"tree /a /f \"{base_local}\" > \"{relatorio_txt}\"")

    print("="*60)
    print(f" SUCESSO! Projeto montado em: {base_local}")
    print("="*60)

if __name__ == "__main__":
    main()