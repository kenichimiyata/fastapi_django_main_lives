import unittest
from models.ocr_model import OCRModel

class TestOCRModel(unittest.TestCase):
    def test_recognize_text(self):
        ocr_model = OCRModel()
        image = Image.new('L', (100, 100))
        text = ocr_model.recognize_text(image)
        self.assertIsInstance(text, str)

if __name__ == "__main__":
    unittest.main()