import os
import sys
import re
from config import settings
from modules import aws_handler, vpn_handler, indesign_parser, ai_agent, sync_manager

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    # Primeiro tenta usar o módulo importado normalmente
    job = settings.JOB
    # Forçar leitura direta do arquivo config/settings.py para evitar cache/import e problemas de encoding
    try:
        settings_file = os.path.join(os.path.dirname(__file__), 'config', 'settings.py')
        # Ler com replace para evitar erros por encoding/BOM
        with open(settings_file, 'r', encoding='utf-8', errors='replace') as f:
            src = f.read()
        print(f"-> DEBUG: trecho inicial de config/settings.py:\n{repr(src[:400])}")
        ns = {}
        exec(compile(src, settings_file, 'exec'), ns)
        if 'JOB' in ns and isinstance(ns['JOB'], dict):
            job = ns['JOB']
            print(f"-> DEBUG: JOB carregado diretamente do arquivo: {repr(job)}")
        else:
            print("-> DEBUG: arquivo carregado, mas 'JOB' não encontrado no namespace")
    except Exception as e:
        print(f"-> DEBUG: falha ao carregar config/settings.py diretamente: {e}")
    
    # Define o caminho absoluto para evitar erros de diretório no Windows
    base_local = os.path.abspath(os.path.join(settings.PATHS['temp_local'], job['nome_projeto']))
    
    print("="*60)
    print(f" INICIANDO AUTOMAÇÃO: {job['nome_projeto']}")
    print("="*60)

    # 1. Criar a árvore de diretórios padrão (Apoio, Impressao, Web...)
    sync_manager.setup_estrutura(base_local)

    # 2. Coleta AWS (Capa e Miolo)
    if settings.MODULOS['aws_input']:
        aws_handler.processar_aws(job, base_local)

    # 3. Coleta Local/VPN (Apoio, Originais, Web)
    if settings.MODULOS['vpn_sync']:
        vpn_handler.processar_local(job, base_local)

    # 4. Análise de Metadados InDesign (Busca por Links e Fontes)
    if settings.MODULOS['indesign_parser']:
        caminho_miolo = os.path.join(base_local, "Impressao/Abertos/Miolo")
        links_necessarios = indesign_parser.run(caminho_miolo)

        # Normaliza e salva lista de links extraídos (únicos, A-Z)
        # Limpeza: extrair nomes válidos via regex ou filtrar caracteres imprimíveis
        COMMON_EXT = r'(?:eps|jpg|jpeg|tif|tiff|png|pdf|zip|xml|psd|otf|ttf|ai|svg|bmp)'
        FNAME_RE = re.compile(r'([^\\/:]+\.' + COMMON_EXT + r')', re.IGNORECASE)

        def clean_name(n):
            if not n:
                return None
            n = str(n).strip()
            # Tenta encontrar o arquivo ignorando todo caminho antes da última barra
            m = FNAME_RE.search(n)
            if m:
                return m.group(1).strip()
            # fallback: manter apenas até encontrar qualquer quebra/espaço duplo
            s = ''.join(ch for ch in n if ch.isprintable())
            s = re.sub(r'\s+', ' ', s).strip()
            return s if s else None

        links_unicos = sorted({clean_name(l) for l in links_necessarios if clean_name(l)})
        links_path = os.path.join(base_local, "links_extracted.txt")
        with open(links_path, 'w', encoding='utf-8') as f:
            for l in links_unicos:
                f.write(l + '\n')
        print(f"-> Lista de links extraídos salva em: {links_path}")

        # Gera lista recursiva de arquivos locais em Impressao/Abertos/Miolo
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
        print(f"-> Lista de arquivos locais (Miolo Abertos) salva em: {arquivos_path}")

        # Comparação: links faltantes (presentes nos INDD mas não nos arquivos locais)
        faltantes = sorted(list(set(links_unicos) - set(arquivos_locais_unicos)))
        faltantes_path = os.path.join(base_local, "faltantes_links.txt")
        with open(faltantes_path, 'w', encoding='utf-8') as f:
            for it in faltantes:
                f.write(it + '\n')
        print(f"-> {len(faltantes)} links ausentes. Lista salva em: {faltantes_path}")

        # Verificação adicional: procurar cada faltante recursivamente em todo base_local
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
        print(f"-> Verificação concluída. {found_count}/{len(faltantes)} faltantes encontrados em algum lugar dentro de {base_local}. Detalhes em: {verificacao_path}")

        # 5. Agente de IA para resolver arquivos ausentes
        if faltantes and settings.MODULOS['ai_agent']:
            print(f"\n--- [!] {len(faltantes)} links ausentes detectados ---")
            print("--- Consultando IA para buscar nos Originais... ---")

            # IA olha para a pasta de Originais que acabamos de popular via VPN
            pasta_originais = os.path.join(base_local, "Impressao/Originais")
            arquivos_originais = os.listdir(pasta_originais) if os.path.exists(pasta_originais) else []

            sugestoes = ai_agent.run(faltantes, arquivos_originais, settings.PATHS['lm_studio_url'], output_dir=base_local)

            # sugestoes já gravadas por ai_agent em analise_ia_links.json no diretório do job
            print("-> Relatório de sugestões da IA gerado na raiz do projeto.")

    # 6. Upload para o Armazenamento Final S3
    if settings.MODULOS['aws_output']:
        print("\n--- Preparado para subir estrutura consolidada para AWS S3 Final ---")
        # Usa destino final configurado em settings (JOB['s3_final_root'])
        # Recarrega settings para pegar mudanças feitas em tempo de execução
        try:
            # Usar o `job` já carregado diretamente do arquivo config/settings.py
            try:
                s3_final_raw = job.get('s3_final_root', '')
                print(f"-> DEBUG: job (from file) = {repr(job)}")
                print(f"-> DEBUG: job['s3_final_root'] raw value: {repr(s3_final_raw)}")
                s3_final = str(s3_final_raw).strip() if s3_final_raw is not None else ''
            except Exception as e:
                print(f"-> DEBUG: erro ao obter job['s3_final_root']: {e}")
                s3_final = ''

            # Fallback: tentar extrair literal diretamente do arquivo caso ainda esteja vazio
            if not s3_final:
                try:
                    settings_file = os.path.join(os.path.dirname(__file__), 'config', 'settings.py')
                    with open(settings_file, 'r', encoding='utf-8', errors='replace') as f:
                        txt = f.read()
                    m = re.search(r'"s3_final_root"\s*:\s*"([^"]*)"', txt)
                    if m:
                        s3_final = m.group(1).strip()
                        print(f"-> DEBUG: extraído via regex de arquivo: {repr(s3_final)}")
                    else:
                        print("-> DEBUG: regex não encontrou s3_final_root no arquivo")
                except Exception as e:
                    print(f"-> DEBUG: erro na leitura regex do settings.py: {e}")
        except Exception as e:
            print(f"-> DEBUG: falha ao recarregar settings: {e}")
        s3_final_raw = settings.JOB.get('s3_final_root', '')
        print(f"-> DEBUG: job['s3_final_root'] raw value: {repr(s3_final_raw)}")
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
                    aws_handler.upload_final(base_local, destino_s3)
            else:
                print("-> Modo automático: iniciando upload...")
                aws_handler.upload_final(base_local, destino_s3)

    # 7. Relatório Final de Armazenamento (Seu antigo comando PowerShell)
    print("\n--- Gerando Resumo de Arquivos (tree) ---")
    relatorio_txt = os.path.join(base_local, "arquivos.txt")
    os.system(f"tree /a /f \"{base_local}\" > \"{relatorio_txt}\"")
    
    print("="*60)
    print(f" SUCESSO! Projeto montado em: {base_local}")
    print("="*60)

if __name__ == "__main__":
    main()