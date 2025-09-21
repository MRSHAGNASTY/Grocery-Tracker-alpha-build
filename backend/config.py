import pytesseract

# Configure Tesseract OCR path (adjust if installed elsewhere)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

DATABASE_URL = "sqlite:///grocery.db"

