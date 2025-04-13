import os, random
from PIL import Image, ImageOps, ImageFilter
import numpy as np

def augment_image(image_path, output_dir, base_filename, augmentation_index):
    """Applies a series of random augmentations to an image."""
    try:
        img = Image.open(image_path).convert('RGB')
        augmented_img = img.copy()

        # Random Rotation (up to 15 degrees)
        if random.random() < 0.7:  # Apply with 70% probability
            angle = random.uniform(-15, 15)
            augmented_img = augmented_img.rotate(angle, fillcolor=(0, 0, 0)) # Fill black for rotated areas

        # Random Translation (shift by up to 10% of size)
        if random.random() < 0.7:
            width, height = augmented_img.size
            tx = random.randint(-int(0.1 * width), int(0.1 * width))
            ty = random.randint(-int(0.1 * height), int(0.1 * height))
            augmented_img = augmented_img.transform(augmented_img.size, Image.AFFINE, (1, 0, tx, 0, 1, ty), fillcolor=(0, 0, 0))

        # Random Mirroring (horizontal or vertical)
        if random.random() < 0.5:
            if random.random() < 0.5:
                augmented_img = ImageOps.mirror(augmented_img)  # Horizontal mirror
            else:
                augmented_img = ImageOps.flip(augmented_img)  # Vertical mirror

        # Random Blurring (small radius)
        if random.random() < 0.5:
            radius = random.uniform(0.5, 1.5)
            augmented_img = augmented_img.filter(ImageFilter.GaussianBlur(radius=radius))

        # Random Noise Addition (subtle)
        if random.random() < 0.3:
            img_array = np.array(augmented_img, dtype=np.float32)
            noise = np.random.normal(0, 10, img_array.shape).astype(np.float32)
            noisy_img_array = np.clip(img_array + noise, 0, 255).astype(np.uint8)
            augmented_img = Image.fromarray(noisy_img_array)

        # Save the augmented image
        new_filename = f"{base_filename}_augmented_{augmentation_index}.{os.path.splitext(os.path.basename(image_path))[1][1:]}"
        output_path = os.path.join(output_dir, new_filename)
        augmented_img.save(output_path)

    except Exception as e:
        print(f"Error augmenting {image_path}: {e}")

def augment_folder(input_folder, output_folder, num_augmentations_per_image=3):
    """Augments all images in the input folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_folder, filename)
            base_filename = os.path.splitext(filename)[0]
            for i in range(num_augmentations_per_image):
                augment_image(image_path, output_folder, base_filename, i)
            print(f"Augmented {filename} {num_augmentations_per_image} times.")

if __name__ == "__main__":
    input_folder = r"C:\Users\niksh\Desktop\normal_raw"  # Replace with the path to your folder of images
    output_folder = r"C:\Users\niksh\Desktop\normal"  # Replace with the path where you want to save augmented images

    num_augmentations_per_image = 3
    augment_folder(input_folder, output_folder, num_augmentations_per_image)
    print(f"Augmentation process completed. Augmented images saved in: {output_folder}")