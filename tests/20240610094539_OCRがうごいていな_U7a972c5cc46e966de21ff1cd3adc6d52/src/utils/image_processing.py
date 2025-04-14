from PIL import Image, ImageEnhance, ImageFilter

def preprocess_image(image_path):
    # Open the image
    image = Image.open(image_path)

    # Convert to grayscale
    image = image.convert('L')

    # Apply thresholding
    image = image.point(lambda x: 0 if x < 140 else 255)

    # Apply binary inversion
    image = image.point(lambda x: 255 - x)

    # Apply median filter
    image = image.filter(ImageFilter.MedianFilter(size=3))

    return image