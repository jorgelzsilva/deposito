# --- MAPEAMENTO MANUAL DE CAMINHOS ---
JOB = {
    "nome_projeto": "9788582606858",
    
    # Raízes AWS
    "s3_capa_root": "s3://workdocs-publishing/Fornecedores/KAELE/kaele/Capas/05646 - Kloppenborg_Gerenciamento de projetos contemporaneos_5ed/",
    "s3_miolo_root": "C:\\Users\\jlsilva\\OneDrive - Grupo A Educação SA\\Controle_backup\\Provisorio_Publishing\\Kloppenborg_Gerenciamento de Projetos Contemporâneos _5ed\\Kloppenborg_Gerenciamento de Projetos Contemporâneos",
    # Bucket final para upload de saída (defina como s3://seu-bucket/Finalizados/)
    "s3_final_root": "s3://workdocs-publishing/BACKUP_PUBLISHING_atual/",
    
    # Raízes VPN/Local (Agora com Originais e Metabooks explícitos)
    "vpn_apoio_root": r"",
    "vpn_originais": r"L:\K\KLOPPENBORG_Timothy\Gerenciamento_de_projetos_5ed\Original",
    "vpn_web_epub":  r"L:\K\KLOPPENBORG_Timothy\Gerenciamento_de_projetos_5ed\Temporario\ePub\Plataformas\binpar",
    "vpn_metabooks": r"L:\K\KLOPPENBORG_Timothy\Gerenciamento_de_projetos_5ed\Temporario\Metabooks"
}

# Flags de ativação de módulos
MODULOS = {
    "aws_input": True,
    "vpn_sync": True,
    "indesign_parser": True,
    "ai_agent": True,
    "aws_output": True
}

# Caminhos de pastas persistentes
PATHS = {
    "temp_local": "./temp",
    "lm_studio_url": "http://192.168.28.70:1234/v1"
}
