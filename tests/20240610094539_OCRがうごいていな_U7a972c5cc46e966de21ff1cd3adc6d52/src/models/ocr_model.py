import pytesseract
from PIL import Image

class OCRModel:
    def __init__(self):
        self.tesseract_config = '-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz --psm 11'

    def recognize_text(self, image):
        # Perform OCR using Tesseract
        text = pytesseract.image_to_string(image, config=self.tesseract_config)
        return text