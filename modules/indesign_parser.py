import re
import os
import unicodedata

COMMON_EXT = r'(?:eps|jpg|jpeg|tif|tiff|png|pdf|zip|xml|psd|otf|ttf|ai|svg|bmp)'
FNAME_RE = re.compile(r'([A-Za-z0-9_\- \(\)\[\]\.]+\.' + COMMON_EXT + r')', re.IGNORECASE)

def get_indesign_links(file_path):
    links = []
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
            # Busca no XML interno do InDesign por nomes de arquivos vinculados
            found = re.findall(rb'<stRef:filePath>(.*?)</stRef:filePath>', content, re.DOTALL)
            for path_bytes in found:
                path_str = None
                # Tentar várias decodificações comuns
                for enc in ('utf-8', 'cp1252', 'latin-1', 'utf-16'):
                    try:
                        path_str = path_bytes.decode(enc)
                        break
                    except Exception:
                        continue
                if path_str is None:
                    # fallback: decodifica ignorando erros
                    try:
                        path_str = path_bytes.decode('utf-8', errors='ignore')
                    except Exception:
                        path_str = str(path_bytes)

                # normaliza barras e remove caracteres nulos/espaços
                path_str = path_str.replace('\\', '/').strip().strip('\x00')

                # Tentar extrair filename com extensão comum via regex
                fname = None
                m = FNAME_RE.search(path_str)
                if m:
                    fname = m.group(1).strip()
                else:
                    # fallback: basename e sanitização
                    candidate = os.path.basename(path_str)
                    if candidate:
                        # Normalizar unicode e remover marcas
                        candidate = unicodedata.normalize('NFKC', candidate)
                        # Remover caracteres de controle / não imprimíveis
                        candidate = ''.join(ch for ch in candidate if ch.isprintable())
                        # Remover caracteres não-ASCII e substituir múltiplos espaços
                        candidate = ''.join(ch for ch in candidate if ord(ch) < 128)
                        candidate = re.sub(r'\s+', ' ', candidate).strip()
                        # Tentar extrair extensão mesmo aqui
                        m2 = FNAME_RE.search(candidate)
                        if m2:
                            fname = m2.group(1).strip()
                        else:
                            fname = candidate

                if fname:
                    # limpeza final: remover espaços extremos e caracteres indesejados
                    fname = fname.strip()
                    # evitar nomes muito longos ou vazios
                    if 0 < len(fname) <= 200:
                        links.append(fname)
    except Exception as e:
        print(f"Erro ao ler InDesign: {e}")
    return list(dict.fromkeys(links))  # Remove duplicados mantendo ordem

def run(pasta_trabalho):
    print("-> Analisando arquivos InDesign...")
    todos_links = []
    for root, dirs, files in os.walk(pasta_trabalho):
        for file in files:
            if file.lower().endswith(".indd"):
                print(f"   Extraindo de: {file}")
                todos_links.extend(get_indesign_links(os.path.join(root, file)))
    return todos_links