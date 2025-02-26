import pdfplumber

# Caminho correto do arquivo PDF
caminho_pdf = "C:\\Users\\samue\\Downloads\\teste.pdf"

try:
    with pdfplumber.open(caminho_pdf) as pdf:
        primeira_pagina = pdf.pages[0]
        texto = primeira_pagina.extract_text()
        print(texto)
except Exception as e:
    print(f"Ocorreu um erro: {e}")
