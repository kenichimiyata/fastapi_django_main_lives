import unittest
from utils.image_processing import preprocess_image

class TestImageProcessing(unittest.TestCase):
    def test_preprocess_image(self):
        image_path = 'path/to/image.jpg'
        image = preprocess_image(image_path)
        self.assertIsInstance(image, Image.Image)

if __name__ == "__main__":
    unittest.main()