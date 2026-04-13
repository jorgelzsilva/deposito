# --- MAPEAMENTO MANUAL DE CAMINHOS ---
JOB = {
    "nome_projeto": "9786558823780",
    
    # Raízes AWS
    "s3_capa_root": "s3://workdocs-publishing/Fornecedores/KAELE/kaele/Capas/05678 - CARDOSO Manual de terapoia de grupo PRISMAS/",
    "s3_miolo_root": "s3://workdocs-publishing/Fornecedores/AGE/age/CARDOSO_Manual_Terapia_Grupo_PRISMAS/",
    # Bucket final para upload de saída (defina como s3://seu-bucket/Finalizados/)
    "s3_final_root": "s3://workdocs-publishing/BACKUP_PUBLISHING_atual/",
    
    # Raízes VPN/Local (Agora com Originais e Metabooks explícitos)
    "vpn_apoio_root": r"",
    "vpn_originais": r"L:\C\CARDOSO_Bruno\Manual_terapia_de_grupo_PRISMAS\Original",
    "vpn_web_epub":  r"L:\C\CARDOSO_Bruno\Manual_terapia_de_grupo_PRISMAS\Temporario\epub\Plataformas\binpar",
    "vpn_metabooks": r"L:\C\CARDOSO_Bruno\Manual_terapia_de_grupo_PRISMAS\Temporario\Metabooks"
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
