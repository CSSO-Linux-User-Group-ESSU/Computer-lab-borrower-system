import cv2
import numpy as np
from PIL import Image
import pytesseract


def preprocess_image(image_path):
    """Load and preprocess the image for better OCR accuracy."""
    try:
        # Read the image using OpenCV
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Image at {image_path} could not be loaded.")

        # Convert the image to the HSV color space
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Define the range for blue color in HSV
        lower_blue = np.array([90, 50, 50])  # Lower bound of blue
        upper_blue = np.array([130, 255, 255])  # Upper bound of blue

        # Create a mask to extract only blue ink
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # The extracted blue ink
        blue_img = cv2.bitwise_and(img,img,mask=mask)

        # Convert the extracted image to grayscale
        gray = cv2.cvtColor(blue_img, cv2.COLOR_BGR2GRAY)


        # Denoise the image using Gaussian Blur
        denoised = cv2.GaussianBlur(gray, (5, 5), 0)


        # Apply binary thresholding (Binarization)
        _, binary_img = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY)


        # Morphological transformation to clean the image
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        cleaned_img = cv2.morphologyEx(binary_img, cv2.MORPH_CLOSE, kernel)

        return cleaned_img
    except Exception as e:
        print(f"Error in preprocess_image: {e}")
        return None

def resize_image(image, scale_factor=2):
    """Resize the image to improve OCR accuracy."""
    try:
        height, width = image.shape
        new_size = (width * scale_factor, height * scale_factor)
        resized_img = cv2.resize(image, new_size, interpolation=cv2.INTER_LINEAR)

        return resized_img
    except Exception as e:
        print(f"Error in resize_image: {e}")
        return image

def ocr_image(image):
    """Perform OCR on the preprocessed image."""
    try:
        pil_img = Image.fromarray(image)

        # Custom configuration for tesseract (LSTM OCR engine, automatic page segmentation)
        custom_config = r'--oem 3 --psm 6'

        # Perform OCR using pytesseract
        text = pytesseract.image_to_string(pil_img, config=custom_config)
        return text
    except Exception as e:
        print(f"Error in ocr_image: {e}")
        return ""

if __name__ == "__main__":

    # Path to the image
    image_path = '/home/davon/Com-lab-borrower-system/Computer-lab-borrower-system/HTR/warren.jpg'

    # Preprocess the image
    preprocessed_img = preprocess_image(image_path)

    if preprocessed_img is not None:
        # Resize the image for better OCR accuracy
        resized_img = resize_image(preprocessed_img)
        
        # Save the processed image 
        cv2.imwrite('HTR/img_blue.jpg', resized_img)

        # Perform OCR on the resized image
        extracted_text = ocr_image(resized_img)

        # Print the extracted text
        print("Extracted Text:")
        print(extracted_text)
    else:
        print("Failed to preprocess the image.")
