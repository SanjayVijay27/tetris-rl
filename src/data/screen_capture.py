import cv2
import numpy as np
from PIL import Image

"""
bounding_box: dictionary containing top and left bounds, width, and height of the bounding box
sct: sct returned by mss()

img: np array representing image within bounding box

captures and returns the image from a given bounding box with sct
"""
def getImage(bounding_box, sct):
    screenShot = sct.grab(bounding_box)

    img = Image.frombytes(
        'RGB', 
        (screenShot.width, screenShot.height), 
        screenShot.rgb, 
    )

    img = np.array(img)[:, :, ::-1].copy()

    return img


"""
img: np array representing an image

contours: list of np arrays representing the contours found within the image

finds and returns contours from a given image
"""
def getContours(img):
    # blur
    blur = cv2.bilateralFilter(img,9,75,75)

    # grayscale
    gray = cv2.cvtColor(np.array(blur), cv2.COLOR_BGR2GRAY)

    # threshold
    thresh = cv2.threshold(gray, 64, 255, cv2.THRESH_BINARY)[1]

    # get contour bounding boxes
    contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    return contours