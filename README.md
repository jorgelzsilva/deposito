# Deposito

Automação para montagem de estrutura de projetos de editoração, sincronizando arquivos entre AWS S3 e servidores locais via VPN. O sistema consolida as pastas padrão (Apoio, Impressão, Web, Metabooks) e utiliza Inteligência Artificial para sugerir substituições de links ausentes detectados nos arquivos InDesign.

## 🚀 Módulos e Componentes

- **`main.py`**: Ponto de entrada principal. Orquestra a execução de todos os módulos, desde a criação da estrutura até o upload final.
- **`config/settings.py`**: Configuração central do projeto, contendo os caminhos (S3 e Local), flags de ativação de módulos e credenciais.
- **`modules/aws_handler.py`**: Gerencia a comunicação com o AWS S3 (download de insumos e upload do projeto finalizado).
- **`modules/vpn_handler.py`**: Responsável por sincronizar arquivos das pastas de Originais e Apoio que residem em servidores locais/VPN.
- **`modules/sync_manager.py`**: Cria a árvore de diretórios padrão do projeto (Apoio, Impressão, Web, etc).
- **`modules/indesign_parser.py`**: Extrai metadados de arquivos `.indd` para identificar dependências de links e fontes.
- **`modules/ai_agent.py`**: Integração com LM Studio para analisar arquivos faltantes e sugerir substitutos baseados nos arquivos disponíveis nos Originais.

## 🛠️ Como Usar

1. Certifique-se de ter o [LM Studio](https://lmstudio.ai/) rodando localmente (se o módulo de IA estiver ativo).
2. Configure o `config/settings.py` com o código do JOB e os caminhos corretos.
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute o script principal:
   ```bash
   python main.py
   ```

## ⚠️ Segurança

Este projeto contém um arquivo `.gitignore` configurado para não expor `config/credentials.json`, pastas `temp/`, logs e ambientes virtuais. Nunca commite dados sensíveis diretamente.
