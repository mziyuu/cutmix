import os
import PIL
from PIL import Image
import random


def generate_paste_location(background_size, target_size):
    pass


def cutmix(background_image, target_image):

    new_image = background_image.copy()
    paste_location = generate_paste_location(background_image.size(), target_image.size())
    new_image.paste(target_image, paste_location)
    new_image.show()


def main():
    person_img = "1.png"
    background = "frame0001.jpg"
    person_image = Image.open(person_img)
    background_image = Image.open(background)
    cutmix(background_image, person_image)

if __name__ == "__main__":
    main()