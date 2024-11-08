import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import cv2
import numpy as np
from PIL import Image
import pytesseract
import argparse
from datetime import datetime

from HTR.aruco_crop import crop_using_aruco as crop

def preprocess_image(image_path, crop_path):
    """Load and preprocess the image for better OCR accuracy."""
    try:
        # Read the image using OpenCV
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Image at {image_path} could not be loaded.")

        cropped = crop(image_path, crop_path)

        # Convert the image to the HSV color space
        hsv = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)

        # Define the range for blue color in HSV
        lower_blue = np.array([90, 50, 100])  # Lower bound of blue
        upper_blue = np.array([130, 255, 255])  # Upper bound of blue

        # Create a mask to extract only blue ink
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # The extracted blue ink
        blue_img = cv2.bitwise_and(cropped,cropped,mask=mask)

        cv2.imwrite('Blue.png', blue_img)

        # Convert the extracted image to grayscale
        gray = cv2.cvtColor(blue_img, cv2.COLOR_BGR2GRAY)


        # Denoise the image using Gaussian Blur
        denoised = cv2.GaussianBlur(gray, (1, 1), 0)


        # Apply binary thresholding (Binarization)
        _, binary_img = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY)


        # Morphological transformation to clean the image
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        cleaned_img = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel)

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
        custom_config = r'-l eng+fil+spa+eng_handwritten --psm 6 --oem 3'

        # Perform OCR using pytesseract
        text = pytesseract.image_to_string(pil_img, config=custom_config)
        return text
    except Exception as e:
        print(f"Error in ocr_image: {e}")
        return ""

if __name__ == "__main__":

    date = str(datetime.now())
    date = date[:-10]
    date = date.replace(' ', '-')
    parser = argparse.ArgumentParser(description='Perform OCR on a scanned image.')
    parser.add_argument('image_path', 
                        type=str, 
                        nargs='?',
                        help='Path to the scanned image file') 
    args = parser.parse_args()

    # Path to the image
    image_path =  args.image_path or 'HTR/scannedImages/scanned_form.png'
    crop_path = f'HTR/croppedImages/Borrow-{date}.jpg'

    # Preprocess the image
    preprocessed_img = preprocess_image(image_path, crop_path)

    if preprocessed_img is not None:
        # Resize the image for better OCR accuracy
        resized_img = resize_image(preprocessed_img)
        
        # Save the processed image 
        cv2.imwrite(f'HTR/processedImages/Borrow-{date}.jpg', resized_img)
        # Save on Training folder
        cv2.imwrite(f'HTR/trainingImages/Borrow-{date}.jpg', resized_img)

        # Perform OCR on the resized image
        extracted_text = ocr_image(resized_img)

        # Print the extracted text.
        print(date)
        print("Extracted Text:")
        print(extracted_text)
        with open('HTR/data/data.txt','wt') as f:
            f.write(extracted_text)
    else:
        print("Failed to preprocess the image.")
