from models.ocr_model import OCRModel
from utils.image_processing import preprocess_image

def main():
    # Load the OCR model
    ocr_model = OCRModel()

    # Load the image
    image_path = 'path/to/image.jpg'
    image = preprocess_image(image_path)

    # Perform OCR
    text = ocr_model.recognize_text(image)

    print("Recognized text:", text)

if __name__ == "__main__":
    main()