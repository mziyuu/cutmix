import os
import PIL
from PIL import Image
person_img = "1.png"
background = "frame0001.jpg"

person_image = Image.open(person_img)
background_image = Image.open(background)
new_image = background_image.copy()
new_image.paste(person_image,)

new_image.show()

print(new_image)
