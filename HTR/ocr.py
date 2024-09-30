import cv2
import numpy as np
from PIL import Image
import pytesseract

def crop_image(image_path):
    """Crop the image for better OCR accuracy"""
    # Read the image using OpenCV
    img = cv2.imread(image_path)

    # Initialize the image dimensions
    height, width, _ = img.shape
    new_height = int(height*.79) # to remove the borrower's sign
    new_width = int(width/2) # to remove unnessesary whitespace
    
    # The Actual cropping of the image
    cropped_img = img[:new_height, :new_width]
    return cropped_img

def preprocess_image(image_path):
    """Load and preprocess the image for better OCR accuracy."""
    try:
        # Crop the image
        img = crop_image(image_path)

        if img is None:
            raise FileNotFoundError(f"Image at {image_path} could not be loaded.")

        # Convert the image to the HSV color space
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Define the range for blue color in HSV
        lower_blue = np.array([92, 120, 120]) 
        upper_blue = np.array([130, 255, 255])  

        # Create a mask to extract only blue ink
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        blue_img = cv2.bitwise_and(img,img,mask=mask)

        # Convert the masked image to grayscale
        gray = cv2.cvtColor(blue_img, cv2.COLOR_BGR2GRAY)

        # Denoise the image using Gaussian Blur
        denoised = cv2.GaussianBlur(gray, (3, 3), 0)

        cv2.imwrite('denoised.jpg', denoised)

        # Apply binary thresholding (Binarization)
        _, binary_img = cv2.threshold(denoised, 10, 255, cv2.THRESH_BINARY)

        cv2.imwrite('binary.jpg',binary_img)

        # Morphological transformation to clean the image
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        cleaned_img = cv2.morphologyEx(binary_img, cv2.MORPH_CLOSE, kernel)

        cv2.imwrite('clean.jpg', cleaned_img)

        return cleaned_img
    except Exception as e:
        print(f"Error in preprocess_image: {e}")
        return None

def resize_image(image, scale_factor=3):
    """Resize the image to improve OCR accuracy."""
    try:
        height, width = image.shape
        size = (width * scale_factor, height * scale_factor)
        new_size = (int(size[0]), int(size[1]))
        resized_img = cv2.resize(image, new_size, interpolation=cv2.INTER_LINEAR)
        cv2.imwrite('resized.jpg', resized_img)
        return resized_img
    except Exception as e:
        print(f"Error in resize_image: {e}")
        return image

def ocr_image(image):
    """Perform OCR on the preprocessed image."""
    try:
        pil_img = Image.fromarray(image)

        # Custom configuration for tesseract
        custom_config = r'--oem 3 --psm 6'

        # Perform OCR using pytesseract
        text = pytesseract.image_to_string(pil_img, config=custom_config)
        return text
    except Exception as e:
        print(f"Error in ocr_image: {e}")
        return ""

if __name__ == "__main__":

    # Path to the image
    image_path = 'HTR/scanme.jpeg'

    # Preprocess the image
    preprocessed_img = preprocess_image(image_path)

    if preprocessed_img is not None:
        # Resize the image for better OCR accuracy
        resized_img = resize_image(preprocessed_img)

        cv2.imwrite('img_blue1.jpg', resized_img)

        # Perform OCR on the resized image
        extracted_text = ocr_image(resized_img)

        # Print the extracted text
        print("Extracted Text:")
        print(extracted_text)
    else:
        print("Failed to preprocess the image.")
