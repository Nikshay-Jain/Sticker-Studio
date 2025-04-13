import os
from PIL import Image

def augment_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_folder, filename)
            try:
                img = Image.open(input_path)
                name, ext = os.path.splitext(filename)

                # Rotation
                angle_acw = 15
                rotated_acw = img.rotate(angle_acw)
                rotated_acw.save(os.path.join(output_folder, f"{name}_rotated_acw{ext}"))

                angle_cw = -15
                rotated_cw = img.rotate(angle_cw)
                rotated_cw.save(os.path.join(output_folder, f"{name}_rotated_cw{ext}"))

                # Mirroring along x-axis (horizontal flip)
                mirrored_x = img.transpose(Image.FLIP_LEFT_RIGHT)
                mirrored_x.save(os.path.join(output_folder, f"{name}_mirrored_x{ext}"))

                # Mirroring along y-axis (vertical flip)
                mirrored_y = img.transpose(Image.FLIP_TOP_BOTTOM)
                mirrored_y.save(os.path.join(output_folder, f"{name}_mirrored_y{ext}"))

                # Mirroring along origin (both x and y flip)
                mirrored_origin = img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)
                mirrored_origin.save(os.path.join(output_folder, f"{name}_mirrored_origin{ext}"))

                print(f"Augmented image: {filename}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    input_directory = r"C:\Users\niksh\Desktop\ghibli"  # Replace with the path to your folder of images
    output_directory = r"C:\Users\niksh\Desktop\ghibli"  # Replace with the path where you want to save augmented images

    for i in range(3):
        augment_images(input_directory, output_directory)
        print(f"\nAugmented images saved in: {output_directory}")