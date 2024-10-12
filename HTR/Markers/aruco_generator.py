import cv2
import numpy as np

# Create a dictionary of ArUco markers
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

# Generate ArUco markers and save them as images
for i in range(4):
    marker = cv2.aruco.generateImageMarker(aruco_dict, i, 30)  # Marker id and size
    cv2.imwrite(f'marker_{i}.png', marker)
