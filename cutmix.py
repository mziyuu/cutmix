import os
import PIL
from PIL import Image
import cv2
import random
from tqdm import tqdm


background_dir = "background"
old_label_dir = "labels"
new_label_dir = "cutmix_labels"
old_image_dir = "images"
new_image_dir = "cutmix_images"
dataset = ["train", "val"]

os.mkdir(new_image_dir)
os.mkdir(new_label_dir)

def calculate_new_bbox(old_bbox, background_size, target_size, paste_location):
    """calculate new bbox
    """
    old_bbox = old_bbox.split(" ")
    old_bbox = [float(x) for x in old_bbox]
    new_label = [
        int(old_bbox[0]),
        (paste_location[0] + target_size[0] * old_bbox[1]) / background_size[0],
        (paste_location[1] + target_size[1] * old_bbox[2]) / background_size[1],
        target_size[0] * old_bbox[3] / background_size[0],
        target_size[1] * old_bbox[4] / background_size[1]
    ]
    new_label_str = ""
    for x in new_label:
        new_label_str += "{} ".format(x)
    new_label_str += "\n"
    return new_label_str


def generate_new_label(label, background_size, target_size, paste_location, old_label_sub_dir, new_label_sub_dir):
    """generate new yolo label file
    """
    with open(os.path.join(old_label_sub_dir, label), 'r') as f:
        old_label = f.readlines()

    with open(os.path.join(new_label_sub_dir, label), "w") as f:
        for old_bbox in old_label:
            new_bbox = calculate_new_bbox(old_bbox, background_size, target_size, paste_location)
            f.writelines(new_bbox)


def generate_paste_location(background_size, target_size):
    """ random generate the location of the image's upper left corner
    """
    x = random.randint(0, background_size[0] - target_size[0])
    y = random.randint(0, background_size[1] - target_size[1])
    return x, y


def cutmix(old_label, background, patch, sub_dataset):
    
    old_label_sub_dir = os.path.join(old_label_dir, sub_dataset)
    new_label_sub_dir = os.path.join(new_label_dir, sub_dataset)
    old_image_sub_dir = os.path.join(old_image_dir, sub_dataset)
    new_image_sub_dir = os.path.join(new_image_dir, sub_dataset)

    image = Image.open(os.path.join(old_image_sub_dir, patch))
    background_image = Image.open(os.path.join(background_dir, background))
    while image.size[0] * 2 > background_image.size[0] or image.size[1] * 2 > background_image.size[1]:
        image = image.resize((int(image.size[0]*0.5), int(image.size[1]*0.5)))
        # pass if patch size * 2 > background size
    new_image = background_image.copy()
    paste_location = generate_paste_location(background_image.size, image.size)
    generate_new_label(old_label, background_image.size, image.size, paste_location, old_label_sub_dir, new_label_sub_dir)
    new_image.paste(image, paste_location)
    new_image.save(os.path.join(new_image_dir, patch))
    return 1


def main():
    
    for sub_dataset in dataset:
        cnt = 0
        old_image_sub_dir = os.path.join(old_image_dir, sub_dataset)
        
        os.mkdir(os.path.join(new_image_dir, sub_dataset))
        os.mkdir(os.path.join(new_label_dir, sub_dataset))
        
        for image in tqdm(os.listdir(old_image_sub_dir)):
            image_name = os.path.split(image)[-1].split(".")[0]
            old_label = "{}.txt".format(image_name)
            background = random.sample(os.listdir(background_dir), 1)[0]
            cnt += cutmix(old_label, background, image, sub_dataset)
        print("{} images generated".format(cnt))
    


if __name__ == "__main__":
    main()
