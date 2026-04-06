import os

def setup_estrutura(base_local):
    """
    Cria a árvore de diretórios padrão para o projeto.
    Apoio, Impressao (Abertos, Fechados, Originais), Web (ePub, Metabooks).
    """
    print(f"-> Criando estrutura de pastas em: {base_local}")
    
    pastas = [
        "Apoio/Lib",
        "Apoio/Res",
        "Impressao/Abertos/Capa",
        "Impressao/Abertos/Miolo",
        "Impressao/Fechados/Capa",
        "Impressao/Fechados/Miolo",
        "Impressao/Originais",
        "Web/ePub",
        "Web/Metabooks"
    ]
    
    for pasta in pastas:
        caminho = os.path.join(base_local, pasta)
        os.makedirs(caminho, exist_ok=True)
        print(f"   [OK] {pasta}")
