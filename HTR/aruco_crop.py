import cv2
import numpy as np

def aruco_crop(image_path, width, height, output_path='cropped_form.png'):
    """
    Crops a specific area of the image using ArUco markers.

    Parameters:
        image_path (str): Path to the scanned image.
        width (int): Desired width of the cropped image.
        height (int): Desired height of the cropped image.
        output_path (str): Path to save the cropped image (default is 'cropped_form.png').
    """
    # Load the scanned image
    img = cv2.imread(image_path)

    # Create a dictionary of ArUco markers
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

    # Detect ArUco markers in the image
    corners, ids, _ = cv2.aruco.detectMarkers(img, aruco_dict)

    if ids is not None:
        # Get the corners of the detected markers
        corners = np.array(corners)

        # Sort the corners based on their IDs (0, 1, 2, 3 for the four markers)
        sorted_corners = [corners[i][0] for i in np.argsort(ids.flatten())]

        # Get the four points of the markers (top-left, top-right, bottom-right, bottom-left)
        src_pts = np.array(sorted_corners, dtype="float32")

        # Define the destination points for cropping
        dst_pts = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype="float32")

        # Compute the perspective transform matrix
        M = cv2.getPerspectiveTransform(src_pts, dst_pts)

        # Apply the perspective transformation to get the cropped form
        cropped = cv2.warpPerspective(img, M, (width, height))

        # Save the cropped image
        cv2.imwrite(output_path, cropped)
    else:
        print("Markers not detected!")

# Example usage
if __name__ == "__main__":
    aruco_crop('scanned_form.png', 1000, 1400)
