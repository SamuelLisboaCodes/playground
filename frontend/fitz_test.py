import fitz

# Abrir um PDF de teste
pdf_document = fitz.open("C:\\Users\\samue\\Downloads\\sodapdf-converted (3).pdf")

# Extrair texto da primeira página
page = pdf_document.load_page(0)
text = page.get_text("text")

print(text)
