import os
import subprocess
import sys

# --- Configuração de Pastas ---
STRUCTURE = [
    "modules",
    "config",
    "temp",
    "prompts",
    "reports"
]

FILES = {
    "config/settings.py": """# Flags de ativação de módulos
MODULOS = {
    "aws_input": True,
    "vpn_sync": True,
    "indesign_parser": True,
    "ai_agent": True,
    "aws_output": True
}

# Caminhos de pastas
PATHS = {
    "temp_local": "./temp",
    "vpn_source": "Z:/Caminho/Da/VPN", # Ajustar conforme sua letra de unidade
    "output_structure": "./temp/organizado"
}
""",
    "config/credentials.json": """{
    "aws_access_key": "SUA_CHAVE_AQUI",
    "aws_secret_key": "SEU_SECRET_AQUI",
    "s3_bucket_in": "bucket-origem",
    "s3_bucket_out": "bucket-destino"
}""",
    "prompts/analise_arquivos.txt": """Você é um assistente de produção editorial. 
Sua tarefa é comparar uma lista de arquivos necessários (extraídos do InDesign) com os arquivos encontrados na pasta local.
Se houver nomes parecidos (ex: 'foto_01.jpg' vs 'foto01_v2.jpg'), sugira a substituição.
Retorne apenas um JSON com as sugestões.""",
    
    "modules/__init__.py": "",
    "modules/ai_agent.py": "def run(): print('AI Agent: Módulo ativado')",
    "modules/aws_handler.py": "def run(): print('AWS Handler: Módulo ativado')",
    "modules/indesign_parser.py": "def run(): print('InDesign Parser: Módulo ativado')",
    
    "main.py": """import os
from config.settings import MODULOS
from modules import aws_handler, indesign_parser, ai_agent

def main():
    print("--- Iniciando Automação Depósito ---")
    
    if MODULOS['aws_input']:
        aws_handler.run()
        
    if MODULOS['indesign_parser']:
        indesign_parser.run()
        
    if MODULOS['ai_agent']:
        ai_agent.run()

    print("--- Processo Finalizado ---")

if __name__ == '__main__':
    main()
"""
}

def create_project():
    print("creating project structure...")
    for folder in STRUCTURE:
        os.makedirs(folder, exist_ok=True)
    
    for path, content in FILES.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    # Criar Ambiente Virtual
    print("Criando ambiente virtual 'deposito'...")
    subprocess.run([sys.executable, "-m", "venv", "deposito"])

    # Comando para instalar bibliotecas (Apenas gera o requirements.txt)
    with open("requirements.txt", "w") as f:
        f.write("boto3\\nrequests\\npython-xmp-toolkit\\ncolorama\\n")

    print("\\n[SUCESSO] Estrutura criada!")
    print("Para começar:")
    print("1. Ative o ambiente: .\\\\deposito\\\\Scripts\\\\activate")
    print("2. Instale as libs: pip install -r requirements.txt")
    print("3. Rode o projeto: python main.py")

if __name__ == "__main__":
    create_project()