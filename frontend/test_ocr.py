from PIL import Image
import pytesseract

# Configura o caminho do executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # ou o caminho correto

# Caminho da imagem no seu sistema
img = Image.open(r"C:\Users\samue\Downloads\Tigre.jpg")  # Certifique-se de que o caminho está correto

# Usa o pytesseract para extrair texto da imagem
text = pytesseract.image_to_string(img)

# Exibe o texto extraído
print(text)
