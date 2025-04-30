import cv2
import os
from PIL import Image # Our new friend for image manipulation and WebP
import hashlib # Import the hashlib library

# Detectron2 imports
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
# No need for Visualizer or MetadataCatalog if we're just getting masks

# --- Configuration for the pre-trained Detectron2 model ---
# Load this configuration once outside the function if segmenting many images
# or load it inside if the script is just for one image at a time.
# For a single script run, loading inside is fine.
cfg = get_cfg()
# Make sure this config file path is correct relative to where you run the script
# or provide an absolute path.
cfg.merge_from_file("detectron2/configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7 # Set a higher threshold for cleaner results
cfg.MODEL.DEVICE = "cpu" # !!! IMPORTANT FOR CPU !!!
# This weight path is a URL, Detectron2 will download it if not found locally.
cfg.MODEL.WEIGHTS = "detectron2://COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x/137849600/model_final_f10217.pkl"

# Create the predictor once
predictor = DefaultPredictor(cfg)
# --- End Configuration ---

def generate_image_hash(image_path):
    """
    Generates a SHA256 hash of the image file content.

    Args:
        image_path (str): The path to the image file.

    Returns:
        str: The hexadecimal representation of the SHA256 hash, or None if file not found.
    """
    if not os.path.exists(image_path):
        print(f"Error: File not found at {image_path} for hashing.")
        return None

    hasher = hashlib.sha256()
    try:
        with open(image_path, 'rb') as f:
            # Read the file in chunks to avoid loading the whole image into memory
            while True:
                chunk = f.read(4096) # Read in 4KB chunks
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        print(f"Error generating hash for {image_path}: {e}")
        return None


def segmentor(image_path, output_dir="segmented images"):
    """
    Loads a pre-trained Detectron2 model, performs instance segmentation,
    isolates the segmented objects, generates a hash for the input image,
    and saves the result as a transparent WebP image using the hash in the filename.

    Args:
        image_path (str): The path to the input image file.
        output_dir (str): The directory where the output transparent WebP will be saved.

    Returns:
        str: The path to the saved WebP file if successful, None otherwise.
    """
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at {image_path}")
        return None

    # Generate hash of the input image
    image_hash = generate_image_hash(image_path)
    if image_hash is None:
        print(f"Could not generate hash for {image_path}. Cannot save with hash filename.")
        return None

    # Construct output path using the hash
    output_webp_path = os.path.join(output_dir, f"{image_hash}.webp")

    # Check if output directory exists, create if not
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")


    # Load the input image using OpenCV
    # Predictor expects a numpy array in BGR format
    print(f"Loading image from {image_path}...")
    im_bgr = cv2.imread(image_path)
    if im_bgr is None:
        print(f"Error: Could not read image from {image_path}")
        return None
    print("Image loaded.")

    # Run the predictor on the image
    print("Running inference (this may take a while on CPU!)...")
    outputs = predictor(im_bgr)
    print("Inference complete.")

    # Extract instance predictions
    instances = outputs["instances"]

    # Check if any instances were detected after filtering by score threshold
    if len(instances) == 0:
        print("No objects detected above the score threshold.")
        # Option: Save a fully transparent image or just exit
        # Let's save a fully transparent image of the original size
        height, width = im_bgr.shape[:2]
        transparent_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        try:
            transparent_img.save(output_webp_path, format='WebP')
            print(f"Saved empty transparent image to {output_webp_path}")
            return output_webp_path
        except Exception as e:
            print(f"Error saving empty transparent image: {e}")
            return None


    # Get the predicted masks. These are boolean tensors/arrays [num_instances, height, width]
    pred_masks = instances.pred_masks.to("cpu").numpy() # Move to CPU and convert to numpy

    # --- Create a composite mask ---
    # Correct Composite Mask: True wherever *any* segmented object exists
    composite_mask = pred_masks.any(axis=0) # This is the mask of the combined foreground objects

    # --- Create a transparent image ---
    # Convert the original BGR image to RGB (Pillow works better with RGB)
    im_rgb = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2RGB)

    # Create a new RGBA image with the same size as the original
    # Initialize with a fully transparent background (0, 0, 0, 0)
    height, width = im_bgr.shape[:2]
    img_rgba = Image.new('RGBA', (width, height), (0, 0, 0, 0))

    # Copy the RGB data from the original image
    img_rgb_pil = Image.fromarray(im_rgb)
    img_rgba.paste(img_rgb_pil, (0, 0))

    # --- Apply the composite mask to the alpha channel ---
    # Convert the boolean composite_mask to an 8-bit grayscale image (0-255)
    # Pixels in the composite_mask that are True (foreground) become 255 (fully opaque)
    # Pixels that are False (background) become 0 (fully transparent)
    alpha_channel = Image.fromarray(composite_mask.astype('uint8') * 255, 'L') # 'L' mode for grayscale

    # Put the new alpha channel into the RGBA image
    img_rgba.putalpha(alpha_channel)

    # --- Save the final image as WebP ---
    try:
        img_rgba.save(output_webp_path, format='WebP')
        print(f"Successfully saved segmented transparent image to {output_webp_path}")
        return output_webp_path
    except Exception as e:
        print(f"Error saving image as WebP: {e}")
        print("Make sure your Pillow installation supports WebP.")
        return None