import cv2
import os
from PIL import Image # Our new friend for image manipulation and WebP

# Detectron2 imports
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
# No need for Visualizer or MetadataCatalog if we're just getting masks

# --- Configuration for the pre-trained Detectron2 model ---
# Load this configuration once outside the function if segmenting many images
# or load it inside if the script is just for one image at a time.
# For a single script run, loading inside is fine.
cfg = get_cfg()
cfg.merge_from_file("detectron2/configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7 # Set a higher threshold for cleaner results
cfg.MODEL.DEVICE = "cpu" # !!! IMPORTANT FOR CPU !!!
cfg.MODEL.WEIGHTS = "detectron2://COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x/137849600/model_final_f10217.pkl"

# Create the predictor once
predictor = DefaultPredictor(cfg)
# --- End Configuration ---


def segment_and_isolate_to_webp(image_path, output_webp_path):
    """
    Loads a pre-trained Detectron2 model, performs instance segmentation,
    isolates the segmented objects, and saves the result as a transparent WebP image.

    Args:
        image_path (str): The path to the input image file.
        output_webp_path (str): The path where the output transparent WebP will be saved.

    Returns:
        bool: True if successful, False otherwise.
    """
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at {image_path}")
        return False

    # Load the input image using OpenCV
    # Predictor expects a numpy array in BGR format
    print(f"Loading image from {image_path}...")
    im_bgr = cv2.imread(image_path)
    if im_bgr is None:
        print(f"Error: Could not read image from {image_path}")
        return False
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
            return True
        except Exception as e:
            print(f"Error saving empty transparent image: {e}")
            return False


    # Get the predicted masks. These are boolean tensors/arrays [num_instances, height, width]
    pred_masks = instances.pred_masks.to("cpu").numpy() # Move to CPU and convert to numpy

    # --- Create a composite mask ---
    # We need a single mask that is TRUE wherever *any* segmented object is.
    # Initialize a blank mask of the same height and width as the image, all False.
    height, width = im_bgr.shape[:2]
    composite_mask = ~pred_masks.any(axis=0) # Logical NOT of (Any mask is TRUE along axis 0)
    # The above line:
    # pred_masks.any(axis=0) -> Gives a [height, width] boolean mask where True means *at least one* instance mask is True at that pixel.
    # ~ (tilde) -> Performs a logical NOT. So composite_mask is True where NO instance mask is True (i.e., the background).
    # Wait, we want the foreground. Let's flip that logic!

    # Correct Composite Mask: True wherever *any* segmented object exists
    composite_mask = pred_masks.any(axis=0) # This is the mask of the combined foreground objects

    # --- Create a transparent image ---
    # Convert the original BGR image to RGB (Pillow works better with RGB)
    im_rgb = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2RGB)

    # Create a new RGBA image with the same size as the original
    # Initialize with a fully transparent background (0, 0, 0, 0)
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
        return True
    except Exception as e:
        print(f"Error saving image as WebP: {e}")
        print("Make sure your Pillow installation supports WebP.")
        return False

# --- How to use the function ---
if __name__ == "__main__":
    # Replace with your input and desired output paths
    input_image_file = "455fc8e4000a3c7ac977ee4c0d484fa20daf559a81d60f3ae719aa7a7303a54a.png"
    output_image_file_webp = "isolated_segment_sticker.webp"

    # Check if the input file exists before proceeding
    if not os.path.exists(input_image_file):
         print(f"Error: Input image not found at {input_image_file}. Please update the path.")
    else:
        success = segment_and_isolate_to_webp(input_image_file, output_image_file_webp)

        if success:
            print("\nProcess finished. Check the output file.")
        else:
             print("\nProcess failed.")
