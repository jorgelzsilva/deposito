(deposito) PS C:\Users\jlsilva\Documents\deposito> python main.py
-> DEBUG: trecho inicial de config/settings.py:
'# --- MAPEAMENTO MANUAL DE CAMINHOS ---\nJOB = {\n    "nome_projeto": "9786558823551",\n    \n    # Raízes AWS\n    "s3_capa_root": "s3://workdocs-publishing/Fornecedores/KAELE/kaele/Capas/Miklowitz_Vivendo Bem com Transtorno Bipolar/",\n    "s3_miolo_root": "s3://workdocs-publishing/Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/",\n    # Bucket final para upload de saída (defin'
-> DEBUG: JOB carregado diretamente do arquivo: {'nome_projeto': '9786558823551', 's3_capa_root': 's3://workdocs-publishing/Fornecedores/KAELE/kaele/Capas/Miklowitz_Vivendo Bem com Transtorno Bipolar/', 's3_miolo_root': 's3://workdocs-publishing/Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/', 's3_final_root': 's3://workdocs-publishing/BACKUP_PUBLISHING_atual/', 'vpn_apoio_root': '', 'vpn_originais': 'L:\\M\\MIKLOWITZ_David_J\\Vivendo_bem_com_transtorno_bipolar\\Original', 'vpn_web_epub': 'L:\\M\\MIKLOWITZ_David_J\\Vivendo_bem_com_transtorno_bipolar\\Temporario\\E-Pub\\Plataformas\\binpar', 'vpn_metabooks': 'L:\\M\\MIKLOWITZ_David_J\\Vivendo_bem_com_transtorno_bipolar\\Temporario\\Metabooks'}
============================================================
 INICIANDO AUTOMAÇÃO: 9786558823551
============================================================
-> Criando estrutura de pastas em: C:\Users\jlsilva\Documents\deposito\temp\9786558823551
   [OK] Apoio/Lib
   [OK] Apoio/Res
   [OK] Impressao/Abertos/Capa
   [OK] Impressao/Abertos/Miolo
   [OK] Impressao/Fechados/Capa
   [OK] Impressao/Fechados/Miolo
   [OK] Impressao/Originais
   [OK] Web/ePub
   [OK] Web/Metabooks

[MÓDULO AWS] Iniciando coleta de materiais (Capa/Miolo)...
   [AWS SYNC] Perfil AWS "publishing" não encontrado. Usando credenciais padrão/variáveis de ambiente.
   [AWS SYNC] Usando credenciais do arquivo config/credentials.json
   [AWS SYNC] Sincronizando: s3://workdocs-publishing/Fornecedores/KAELE/kaele/Capas/Miklowitz_Vivendo Bem com Transtorno Bipolar/Aberto/ -> C:\Users\jlsilva\Documents\deposito\temp\9786558823551/Impressao/Abertos/Capa
   [AWS SYNC] Perfil AWS "publishing" não encontrado. Usando credenciais padrão/variáveis de ambiente.
   [AWS SYNC] Usando credenciais do arquivo config/credentials.json
   [AWS SYNC] Sincronizando: s3://workdocs-publishing/Fornecedores/KAELE/kaele/Capas/Miklowitz_Vivendo Bem com Transtorno Bipolar/Fechado/ -> C:\Users\jlsilva\Documents\deposito\temp\9786558823551/Impressao/Fechados/Capa
   [AWS SYNC] Perfil AWS "publishing" não encontrado. Usando credenciais padrão/variáveis de ambiente.
   [AWS SYNC] Usando credenciais do arquivo config/credentials.json
   [AWS SYNC] Sincronizando: s3://workdocs-publishing/Fornecedores/KAELE/kaele/Capas/Miklowitz_Vivendo Bem com Transtorno Bipolar/Imagens/ -> C:\Users\jlsilva\Documents\deposito\temp\9786558823551/Impressao/Apoio/Capa
   [AWS SYNC] Perfil AWS "publishing" não encontrado. Usando credenciais padrão/variáveis de ambiente.
   [AWS SYNC] Usando credenciais do arquivo config/credentials.json
   [AWS SYNC] Sincronizando: s3://workdocs-publishing/Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/ -> C:\Users\jlsilva\Documents\deposito\temp\9786558823551/Impressao/Abertos/Miolo
   [AWS SYNC] Perfil AWS "publishing" não encontrado. Usando credenciais padrão/variáveis de ambiente.
   [AWS SYNC] Usando credenciais do arquivo config/credentials.json
   [AWS SYNC] Sincronizando: s3://workdocs-publishing/Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Fechados/Miolo/ -> C:\Users\jlsilva\Documents\deposito\temp\9786558823551/Impressao/Fechados/Miolo
   [AWS SYNC] Perfil AWS "publishing" não encontrado. Usando credenciais padrão/variáveis de ambiente.
   [AWS SYNC] Usando credenciais do arquivo config/credentials.json
   [AWS SYNC] Sincronizando: s3://workdocs-publishing/Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Original/ -> C:\Users\jlsilva\Documents\deposito\temp\9786558823551/Impressao/Originais
   [AWS SYNC] Perfil AWS "publishing" não encontrado. Usando credenciais padrão/variáveis de ambiente.
   [AWS SYNC] Usando credenciais do arquivo config/credentials.json
   [AWS SYNC] Nenhum objeto encontrado em s3://workdocs-publishing/Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Original/
   [AWS SYNC] Tentando listar objetos próximos ao prefix: s3://workdocs-publishing/Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/ (debug)
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Capa/
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/C01/Links/C01P25a.eps
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/C01/Links/C01P25b.eps
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/C01/Links/C01P28.eps
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/C01/Miklovitz_C01.indd
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/C02/Links/C02P41.eps
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/C02/Miklovitz_C02.indd
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/C03/Links/C03P52.eps
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/C03/Miklovitz_C03.indd
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/C04/Links/C04P67.eps
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/C04/Miklovitz_C04.indd
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/C05/Miklovitz_C05.indd
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/C06/Miklovitz_C06.indd
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/C07/Miklovitz_C07.indd
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/C08/Miklovitz_C08.indd
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/C09/Links/C09P155.eps
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/C09/Miklovitz_C09.indd
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/C10/Miklovitz_C10.indd
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/C11/Links/C11P181a.eps
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/C11/Links/C11P181b.eps
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/C11/Links/C11P182.eps
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/C11/Miklovitz_C11.indd
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/C12/Miklovitz_C12.indd
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/C13/Miklovitz_C13.indd
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/C14/Miklovitz_C14.indd
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Finais/Miklovitz_Bibliografia.indd
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Finais/Miklovitz_Indice.indd
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Fontes/Kiperman-Bold.ttf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Fontes/Kiperman-BoldItalic.ttf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Fontes/Kiperman-Italic.ttf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Fontes/Kiperman-Regular.ttf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Fontes/Leitura Symbols Arrows.otf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Fontes/Noah Black Italic.otf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Fontes/Noah Black.otf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Fontes/Noah Bold Italic.otf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Fontes/Noah Bold.otf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Fontes/Noah ExtraBold Italic.otf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Fontes/Noah ExtraBold.otf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Fontes/Noah Heavy Italic.otf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Fontes/Noah Heavy.otf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Fontes/Noah Light Italic.otf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Fontes/Noah Light.otf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Fontes/Noah Medium Italic.otf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Fontes/Noah Medium.otf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Fontes/Noah Regular Italic.otf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Fontes/Noah Regular.otf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Fontes/Noah Thin Italic.otf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Fontes/Noah Thin.otf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Fontes/Noah UltraLight Italic.otf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Fontes/Noah UltraLight.otf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Fontes/bakeshop-regular-non-connect.ttf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Iniciais/Links/ABDR_CBL.eps
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Iniciais/Links/Selo_Artmed_FundoClaro.eps
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Iniciais/Miklovitz_Iniciais.indd
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Introducao/Links/IntroP10.eps
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Introducao/Miklovitz_Introducao.indd
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Links_comuns/abertura_base.eps
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Links_comuns/abertura_topo.eps
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Links_comuns/caps.eps
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Links_comuns/duvida.eps
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/Links_comuns/resolucao.eps
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Abertos/Miolo/_Livro_Miklovitz.indb
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Fechados/Capa/
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Fechados/Miolo/Miklovitz_Bibliografia.pdf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Fechados/Miolo/Miklovitz_C01.pdf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Fechados/Miolo/Miklovitz_C02.pdf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Fechados/Miolo/Miklovitz_C03.pdf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Fechados/Miolo/Miklovitz_C04.pdf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Fechados/Miolo/Miklovitz_C05.pdf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Fechados/Miolo/Miklovitz_C06.pdf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Fechados/Miolo/Miklovitz_C07.pdf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Fechados/Miolo/Miklovitz_C08.pdf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Fechados/Miolo/Miklovitz_C09.pdf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Fechados/Miolo/Miklovitz_C10.pdf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Fechados/Miolo/Miklovitz_C11.pdf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Fechados/Miolo/Miklovitz_C12.pdf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Fechados/Miolo/Miklovitz_C13.pdf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Fechados/Miolo/Miklovitz_C14.pdf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Fechados/Miolo/Miklovitz_Completo.pdf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Fechados/Miolo/Miklovitz_Indice.pdf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Fechados/Miolo/Miklovitz_Iniciais.pdf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Fechados/Miolo/Miklovitz_Introducao.pdf
      [DBG] Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/Originais/Guil_Miklowitz_LivingWellBipolarDisorder_Reprodução_do_Livro.pdf
   [AWS SYNC] Usando fallback com prefix comum detectado: s3://workdocs-publishing/Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/Impressao/
-> Iniciando coleta de arquivos locais (VPN/OneDrive)...
   [LOCAL] Tentando: Lib -> C:\Users\jlsilva\Documents\deposito\temp\9786558823551/Apoio/Lib
   [LOCAL] Iniciando cópia: Lib -> C:\Users\jlsilva\Documents\deposito\temp\9786558823551/Apoio/Lib
   [AVISO] Caminho não encontrado: Lib
   [LOCAL] Tentando: Res -> C:\Users\jlsilva\Documents\deposito\temp\9786558823551/Apoio/Res
   [LOCAL] Iniciando cópia: Res -> C:\Users\jlsilva\Documents\deposito\temp\9786558823551/Apoio/Res
   [AVISO] Caminho não encontrado: Res
   [LOCAL] Tentando: L:\M\MIKLOWITZ_David_J\Vivendo_bem_com_transtorno_bipolar\Original -> C:\Users\jlsilva\Documents\deposito\temp\9786558823551/Impressao/Originais
   [LOCAL] Iniciando cópia: L:\M\MIKLOWITZ_David_J\Vivendo_bem_com_transtorno_bipolar\Original -> C:\Users\jlsilva\Documents\deposito\temp\9786558823551/Impressao/Originais
   [LOCAL] 38 arquivos para copiar...
   [LOCAL] Copiando: 9781462555246.epub
   [LOCAL] Copiando: Guil_Miklowitz_LivingWellBipolarDisorder_Reprodução_do_Livro.pdf
   [LOCAL] Copiando: Guil_Miklowitz_LivingWellBipolarDisorder_Reprodução_do_Livro.zip
   [LOCAL] Copiando: Thumbs.db
   [LOCAL] Copiando: Limpos\00_Miklowitz_Praise for Living Well with Bipolar Disorder_Iniciais.docx
   [LOCAL] Copiando: Limpos\01_Miklowitz_Praise for Living Well with Bipolar Disorder_CAP_01.docx
   [LOCAL] Copiando: Limpos\02_Miklowitz_Praise for Living Well with Bipolar Disorder_CAP_02.docx
   [LOCAL] Copiando: Limpos\03_Miklowitz_Praise for Living Well with Bipolar Disorder_CAP_03.docx
   [LOCAL] Copiando: Limpos\04_Miklowitz_Praise for Living Well with Bipolar Disorder_CAP_04.docx
   [LOCAL] Copiando: Limpos\05_Miklowitz_Praise for Living Well with Bipolar Disorder_CAP_05.docx
   [LOCAL] Copiando: Limpos\06_Miklowitz_Praise for Living Well with Bipolar Disorder_CAP_06.docx
   [LOCAL] Copiando: Limpos\07_Miklowitz_Praise for Living Well with Bipolar Disorder_CAP_07.docx
   [LOCAL] Copiando: Limpos\08_Miklowitz_Praise for Living Well with Bipolar Disorder_CAP_08.docx
   [LOCAL] Copiando: Limpos\09_Miklowitz_Praise for Living Well with Bipolar Disorder_CAP_09.docx
   [LOCAL] Copiando: Limpos\10_Miklowitz_Praise for Living Well with Bipolar Disorder_CAP_10.docx
   [LOCAL] Copiando: Limpos\11_Miklowitz_Praise for Living Well with Bipolar Disorder_CAP_11.docx
   [LOCAL] Copiando: Limpos\12_Miklowitz_Praise for Living Well with Bipolar Disorder_CAP_12.docx
   [LOCAL] Copiando: Limpos\13_Miklowitz_Praise for Living Well with Bipolar Disorder_CAP_13.docx
   [LOCAL] Copiando: Limpos\14_Miklowitz_Praise for Living Well with Bipolar Disorder_CAP_14.docx
   [LOCAL] Copiando: Limpos\15_Miklowitz_Praise for Living Well with Bipolar Disorder_Índice.docx
   [LOCAL] Copiando: Pré-traduzidos\00_Miklowitz_Praise for Living Well with Bipolar Disorder_Iniciais_22Laudas.docx
   [LOCAL] Copiando: Pré-traduzidos\01_Miklowitz_Praise for Living Well with Bipolar Disorder_CAP_01_20Laudas.docx
   [LOCAL] Copiando: Pré-traduzidos\02_Miklowitz_Praise for Living Well with Bipolar Disorder_CAP_02_17Laudas.docx
   [LOCAL] Copiando: Pré-traduzidos\03_Miklowitz_Praise for Living Well with Bipolar Disorder_CAP_03_14Laudas.docx
   [LOCAL] Copiando: Pré-traduzidos\04_Miklowitz_Praise for Living Well with Bipolar Disorder_CAP_04_18Laudas.docx
   [LOCAL] Copiando: Pré-traduzidos\05_Miklowitz_Praise for Living Well with Bipolar Disorder_CAP_05_19Laudas.docx
   [LOCAL] Copiando: Pré-traduzidos\06_Miklowitz_Praise for Living Well with Bipolar Disorder_CAP_06_19Laudas.docx
   [LOCAL] Copiando: Pré-traduzidos\07_Miklowitz_Praise for Living Well with Bipolar Disorder_CAP_07_18Laudas.docx
   [LOCAL] Copiando: Pré-traduzidos\08_Miklowitz_Praise for Living Well with Bipolar Disorder_CAP_08_19Laudas.docx
   [LOCAL] Copiando: Pré-traduzidos\09_Miklowitz_Praise for Living Well with Bipolar Disorder_CAP_09_16Laudas.docx
   [LOCAL] Copiando: Pré-traduzidos\10_Miklowitz_Praise for Living Well with Bipolar Disorder_CAP_10_11Laudas.docx
   [LOCAL] Copiando: Pré-traduzidos\11_Miklowitz_Praise for Living Well with Bipolar Disorder_CAP_11_20Laudas.docx
   [LOCAL] Copiando: Pré-traduzidos\12_Miklowitz_Praise for Living Well with Bipolar Disorder_CAP_12_16Laudas.docx
   [LOCAL] Copiando: Pré-traduzidos\13_Miklowitz_Praise for Living Well with Bipolar Disorder_CAP_13_21Laudas.docx
   [LOCAL] Copiando: Pré-traduzidos\14_Miklowitz_Praise for Living Well with Bipolar Disorder_CAP_14_15Laudas.docx
   [LOCAL] Copiando: Pré-traduzidos\15_Miklowitz_Praise for Living Well with Bipolar Disorder_Índice_16Laudas.docx
   [LOCAL] Copiando: Pré-traduzidos\Autor_01Lauda.docx
   [LOCAL] Copiando: Pré-traduzidos\Miklowitz_Pre_Traducao.zip
   [LOCAL] Copiados 38/38 arquivos - 24s
   [LOCAL] Concluído: 38 arquivos copiados de L:\M\MIKLOWITZ_David_J\Vivendo_bem_com_transtorno_bipolar\Original
   [LOCAL] Tentando: L:\M\MIKLOWITZ_David_J\Vivendo_bem_com_transtorno_bipolar\Temporario\E-Pub\Plataformas\binpar -> C:\Users\jlsilva\Documents\deposito\temp\9786558823551/Web/ePub
   [LOCAL] Iniciando cópia: L:\M\MIKLOWITZ_David_J\Vivendo_bem_com_transtorno_bipolar\Temporario\E-Pub\Plataformas\binpar -> C:\Users\jlsilva\Documents\deposito\temp\9786558823551/Web/ePub
   [LOCAL] 2 arquivos para copiar...
   [LOCAL] Copiando: 9786558823568.epub
   [LOCAL] Copiando: 9786558823568_capa.png
   [LOCAL] Copiados 2/2 arquivos - 1s
   [LOCAL] Concluído: 2 arquivos copiados de L:\M\MIKLOWITZ_David_J\Vivendo_bem_com_transtorno_bipolar\Temporario\E-Pub\Plataformas\binpar
   [LOCAL] Tentando: L:\M\MIKLOWITZ_David_J\Vivendo_bem_com_transtorno_bipolar\Temporario\Metabooks -> C:\Users\jlsilva\Documents\deposito\temp\9786558823551/Web/Metabooks
   [LOCAL] Iniciando cópia: L:\M\MIKLOWITZ_David_J\Vivendo_bem_com_transtorno_bipolar\Temporario\Metabooks -> C:\Users\jlsilva\Documents\deposito\temp\9786558823551/Web/Metabooks
   [LOCAL] 9 arquivos para copiar...
   [LOCAL] Copiando: 9786558823551_capa.png
   [LOCAL] Copiando: 9786558823551_ensaiodeleitura.pdf
   [LOCAL] Copiando: 9786558823551_quartacapa.png
   [LOCAL] Copiando: 9786558823551_sumario.txt
   [LOCAL] Copiando: 9786558823551_vi_01.png
   [LOCAL] Copiando: 9786558823551_vi_02.png
   [LOCAL] Copiando: 9786558823551_vi_03.png
   [LOCAL] Copiando: 9786558823551_vi_04.png
   [LOCAL] Copiando: Thumbs.db
   [LOCAL] Copiados 9/9 arquivos - 3s
   [LOCAL] Concluído: 9 arquivos copiados de L:\M\MIKLOWITZ_David_J\Vivendo_bem_com_transtorno_bipolar\Temporario\Metabooks
-> Analisando arquivos InDesign...
   Extraindo de: Miklovitz_C01.indd
   Extraindo de: Miklovitz_C02.indd
   Extraindo de: Miklovitz_C03.indd
   Extraindo de: Miklovitz_C04.indd
   Extraindo de: Miklovitz_C05.indd
   Extraindo de: Miklovitz_C06.indd
   Extraindo de: Miklovitz_C07.indd
   Extraindo de: Miklovitz_C08.indd
   Extraindo de: Miklovitz_C09.indd
   Extraindo de: Miklovitz_C10.indd
   Extraindo de: Miklovitz_C11.indd
   Extraindo de: Miklovitz_C12.indd
   Extraindo de: Miklovitz_C13.indd
   Extraindo de: Miklovitz_C14.indd
   Extraindo de: Miklovitz_Bibliografia.indd
   Extraindo de: Miklovitz_Indice.indd
   Extraindo de: Miklovitz_Iniciais.indd
   Extraindo de: Miklovitz_Introducao.indd
-> Lista de links extraídos salva em: C:\Users\jlsilva\Documents\deposito\temp\9786558823551\links_extracted.txt
-> Lista de arquivos locais (Miolo Abertos) salva em: C:\Users\jlsilva\Documents\deposito\temp\9786558823551\files_local_miolo.txt
-> 0 links ausentes. Lista salva em: C:\Users\jlsilva\Documents\deposito\temp\9786558823551\faltantes_links.txt
-> Verificação concluída. 0/0 faltantes encontrados em algum lugar dentro de C:\Users\jlsilva\Documents\deposito\temp\9786558823551. Detalhes em: C:\Users\jlsilva\Documents\deposito\temp\9786558823551\faltantes_verificados.txt

--- Preparado para subir estrutura consolidada para AWS S3 Final ---
-> DEBUG: job (from file) = {'nome_projeto': '9786558823551', 's3_capa_root': 's3://workdocs-publishing/Fornecedores/KAELE/kaele/Capas/Miklowitz_Vivendo Bem com Transtorno Bipolar/', 's3_miolo_root': 's3://workdocs-publishing/Fornecedores/MATRIZ/matriz/MIKLOWITZ_Vivendo bem com transtorno bipolar/', 's3_final_root': 's3://workdocs-publishing/BACKUP_PUBLISHING_atual/', 'vpn_apoio_root': '', 'vpn_originais': 'L:\\M\\MIKLOWITZ_David_J\\Vivendo_bem_com_transtorno_bipolar\\Original', 'vpn_web_epub': 'L:\\M\\MIKLOWITZ_David_J\\Vivendo_bem_com_transtorno_bipolar\\Temporario\\E-Pub\\Plataformas\\binpar', 'vpn_metabooks': 'L:\\M\\MIKLOWITZ_David_J\\Vivendo_bem_com_transtorno_bipolar\\Temporario\\Metabooks'}
-> DEBUG: job['s3_final_root'] raw value: 's3://workdocs-publishing/BACKUP_PUBLISHING_atual/'
-> DEBUG: job['s3_final_root'] raw value: 's3://workdocs-publishing/BACKUP_PUBLISHING_atual/'
-> Upload pausado aguardando sinal verde.
   Crie o arquivo 'UPLOAD_OK' na pasta do projeto ou defina a variável de ambiente AUTO_UPLOAD=1 para subir automaticamente.
Pressione 's' e Enter para subir agora, ou qualquer outra tecla para pular: f
-> Upload final PULADO pelo usuário.