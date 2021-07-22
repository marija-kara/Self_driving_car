import cv2, os
import numpy as np
import matplotlib.image as mpimg

def crop(img, crop_size=60):

    new_slika = img.copy()
    cropped = new_slika[crop_size:, :, :]

    return cropped

image_width = 200
image_height = 66

def resize_image(image):
    """
    Resize the image to the input shape used by the network model
    """
    return cv2.resize(image, (image_width, image_height), cv2.INTER_AREA)

def preprocess(image):
    """
    Combine all preprocess functions into one
    """
    image = crop(image)
    image = resize_image(image)
    image = image.astype(np.float32)
    image = image/255.0

    return image
