import os
import argparse
from PIL import Image


def get_image_files(folder):
    valid_extensions = ['.png', '.jpeg', '.jpg']
    return [os.path.join(folder, f) for f in os.listdir(folder) 
            if os.path.splitext(f)[1].lower() in valid_extensions]


def resize_image(image_path, width, height):
    img = Image.open(image_path)
    return img.resize((width, height), Image.Resampling.LANCZOS)


def create_blank_image(width, height, color=(0, 0, 0)):
    return Image.new("RGB", (width, height), color)


def main(folder, width, height, merge_width, merge_height):
    image_files = get_image_files(folder)    
    images_needed = (merge_width // width) * (merge_height // height)
    
    resized_images = []
    for i, image_file in enumerate(image_files):
        if i >= images_needed:
            break
        resized_images.append(resize_image(image_file, width, height))
    

    while len(resized_images) < images_needed:
        resized_images.append(create_blank_image(width, height))
    
    canvas = Image.new('RGB', (merge_width, merge_height), (0, 0, 0))
    
    for i, img in enumerate(resized_images):
        x_offset = (i % (merge_width // width)) * width
        y_offset = (i // (merge_width // width)) * height
        canvas.paste(img, (x_offset, y_offset))
    
    canvas.save(os.path.join(folder, "output_image.jpg"), "JPEG")
    print("output_image.jpg has been created.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resize and merge images.")
    parser.add_argument("--folder", type=str, required=True, help="Folder containing images")
    parser.add_argument("--width", type=int, required=True, help="Width of each resized image")
    parser.add_argument("--height", type=int, required=True, help="Height of each resized image")
    parser.add_argument("--merge-width", type=int, required=True, help="Width of the merged image")
    parser.add_argument("--merge-height", type=int, required=True, help="Height of the merged image")
    
    args = parser.parse_args()
    
    main(args.folder, args.width, args.height, args.merge_width, args.merge_height)
