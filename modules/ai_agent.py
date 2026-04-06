import requests
import json
import time
import difflib
import os
import re
from datetime import datetime

def _save_report(data, filename_base="analise_ia_links"):
    reports_dir = os.path.join(os.getcwd(), 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    json_path = os.path.join(reports_dir, f"{filename_base}_{timestamp}.json")
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"-> Relatório salvo em: {json_path}")
    except Exception as e:
        print(f"-> Erro ao salvar relatório: {e}")

def sugerir_substituicao(arquivos_faltantes, arquivos_disponiveis, url_api, retries=3, timeout=10):
    prompt_sys = ''
    try:
        prompt_sys = open(os.path.join('prompts', 'analise_arquivos.txt'), 'r', encoding='utf-8').read()
    except Exception:
        prompt_sys = ''

    user_msg = f"Faltam: {arquivos_faltantes}. Disponíveis na pasta: {arquivos_disponiveis}"

    payload = {
        "model": "local-model",
        "messages": [
            {"role": "system", "content": prompt_sys},
            {"role": "user", "content": user_msg}
        ],
        "temperature": 0.1
    }

    last_err = None
    for attempt in range(1, retries + 1):
        try:
            resp = requests.post(f"{url_api}/chat/completions", json=payload, timeout=timeout)
            if resp.status_code == 200:
                j = resp.json()
                # tenta extrair conteúdo no formato esperado
                try:
                    content = j['choices'][0]['message']['content']

                    # Tentar extrair JSON se estiver dentro de fences ```json
                    json_text = None
                    m = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
                    if m:
                        json_text = m.group(1)
                    else:
                        # talvez já seja JSON puro
                        json_text = content.strip()

                    parsed = None
                    try:
                        parsed = json.loads(json_text)
                    except Exception as e:
                        # não conseguiu parsear, tratar como vazio
                        parsed = None

                    if parsed and isinstance(parsed, dict) and parsed.get('suggestions'):
                        # Salva relatório com source lm_studio
                        out = {"suggestions_raw": content, "parsed": parsed, "source": "lm_studio", "timestamp": datetime.now().isoformat()}
                        _save_report(out, filename_base="analise_ia_links_lmstudio")
                        return json.dumps(parsed, ensure_ascii=False, indent=2)
                    else:
                        print("-> LM Studio retornou sugestões vazias ou inválidas. Será gerado fallback local.")
                        last_err = Exception('empty_or_invalid_response')
                        # não retornar; sair do loop e executar fallback
                        break

                except Exception as e:
                    last_err = e
                    print(f"-> Resposta inesperada do LM Studio: {e}")
            else:
                last_err = Exception(f"status_code={resp.status_code} body={resp.text}")
                print(f"-> Tentativa {attempt}/{retries} falhou: {last_err}")
        except Exception as e:
            last_err = e
            print(f"-> Tentativa {attempt}/{retries} erro: {e}")
        time.sleep(1 * attempt)

    # Fallback local: fuzzy matching
    print("-> LM Studio indisponível ou retornou vazio. Gerando sugestões locais por similaridade...")
    # Normalizar faltantes: nomes únicos ordenados A-Z
    faltantes_unicos = sorted({str(x).strip() for x in arquivos_faltantes if x})

    # Preparar lista de disponíveis normalizada (basenames)
    disponiveis_norm = [str(x).strip() for x in arquivos_disponiveis if x]

    suggestions = []
    for faltante in faltantes_unicos:
        # pegar candidatos mais próximos (mais permissivo) e também incluir correspondências exatas
        matches = []
        if faltante in disponiveis_norm:
            matches = [faltante]
        else:
            matches = difflib.get_close_matches(faltante, disponiveis_norm, n=10, cutoff=0.2)

        scored = []
        for m in matches:
            ratio = difflib.SequenceMatcher(None, faltante, m).ratio()
            scored.append({"file": m, "score": round(ratio, 3)})

        suggestions.append({"missing": faltante, "matches": scored})

    result = {"suggestions": suggestions, "source": "fallback", "error": str(last_err) if last_err else None, "timestamp": datetime.now().isoformat()}
    _save_report(result)
    return json.dumps(result, ensure_ascii=False, indent=2)

def run(faltantes, disponiveis, url, output_dir=None):
    print("-> Consultando IA para arquivos ausentes...")
    result_str = sugerir_substituicao(faltantes, disponiveis, url)

    # Tentar salvar uma cópia no diretório do job (temp/<job>) se informado
    if output_dir:
        try:
            os.makedirs(output_dir, exist_ok=True)
            out_path = os.path.join(output_dir, "analise_ia_links.json")
            # result_str já é uma string JSON
            with open(out_path, 'w', encoding='utf-8') as f:
                if isinstance(result_str, str):
                    f.write(result_str)
                else:
                    json.dump(result_str, f, ensure_ascii=False, indent=2)
            print(f"-> Relatório salvo também em: {out_path}")
        except Exception as e:
            print(f"-> Erro ao salvar relatório no diretório do job: {e}")

    return result_str