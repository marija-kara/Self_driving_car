import cv2, os
import numpy as np
import matplotlib.image as mpimg

def crop(img, crop_size=60):

    new_slika = img.copy()
    cropped = new_slika[crop_size:, :, :]

    return cropped


def preprocess(image):
    """
    Combine all preprocess functions into one
    """
    image = crop(image)
    image = image.astype(np.float32)
    image = image/255.0

    return image
