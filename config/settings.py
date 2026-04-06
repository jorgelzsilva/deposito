# --- MAPEAMENTO MANUAL DE CAMINHOS ---
JOB = {
    "nome_projeto": "9786558823636",
    
    # Raízes AWS
    "s3_capa_root": "s3://workdocs-publishing/Fornecedores/KAELE/kaele/Capas/Grandin_Autismo_e_adolescencia/",
    "s3_miolo_root": "s3://workdocs-publishing/Fornecedores/CLIC/clic/Grandin_Adolescencia_FINAL/",
    # Bucket final para upload de saída (defina como s3://seu-bucket/Finalizados/)
    "s3_final_root": "s3://workdocs-publishing/BACKUP_PUBLISHING_atual/",
    
    # Raízes VPN/Local (Agora com Originais e Metabooks explícitos)
    "vpn_apoio_root": r"",
    "vpn_originais": r"L:\G\GRANDIN_Temple\Autismo_adolescencia\Original",
    "vpn_web_epub":  r"L:\G\GRANDIN_Temple\Autismo_adolescencia\Temporario\Plataformas\binpar",
    "vpn_metabooks": r"L:\G\GRANDIN_Temple\Autismo_adolescencia\Temporario\Metabooks"
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