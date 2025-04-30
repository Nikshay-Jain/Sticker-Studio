# segment_image_hardcoded_corrected.py
from ultralytics import YOLO
import cv2
import os
import time
import numpy as np # <-- Moved the numpy import here!

def segment_image_from_url(image_url: str, output_dir: str = "segmented_output_hardcoded"):
    """
    Segments objects in an image fetched from a URL using a pre-trained YOLOv8 segmentation model.

    Args:
        image_url: URL of the input image file.
        output_dir: Directory to save the segmented image(s). Defaults to 'segmented_output_hardcoded'.
    """
    # --- Load the Pre-trained YOLOv8 Segmentation Model ---
    # The same model with the learned audacity to understand pixels.
    model = YOLO('models/yolov8n-seg.pt')

    # --- Perform Inference Directly from URL ---
    # Feed the URL directly! Ultralytics handles the fetching.
    print(f"Running inference on image from URL: {image_url}...")
    # This call dives into the network/computational rabbit hole
    # to get the image and then segment it.
    results = model(image_url)

    # --- Process Results and Save Output ---
    print("Processing results...")
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    if results:
        result = results[0] # Assuming the URL resolves to a single image

        if result.masks is not None:
            annotated_img = result.plot()

            # Construct a unique output path based on timestamp
            timestamp = int(time.time())
            output_filename = f"segmented_image_{timestamp}.png" # Using PNG as it's lossless
            output_path = os.path.join(output_dir, output_filename)

            # Save the annotated image
            # YOLO's plot might return a PIL image or a numpy array (cv2 compatible)
            # Ensure it's in the right format for cv2.imwrite

            # The check and conversion logic (now that np is always imported)
            if isinstance(annotated_img, list): # Handle potential list output from plot
                 if len(annotated_img) > 0:
                      # Assuming the first item in the list is the image data
                      # This might need adjustment based on exact plot() output structure
                      annotated_img = annotated_img[0]

            # Convert to numpy array if it's not already (safer check now)
            if not isinstance(annotated_img, np.ndarray):
                # Attempt conversion if it's not already a numpy array
                # This might be needed if plot() returns a PIL Image, for example
                try:
                     annotated_img = np.array(annotated_img)
                     # If converting from PIL, might need to handle color channels
                     if annotated_img.ndim == 3 and annotated_img.shape[2] == 3:
                         # Convert RGB (PIL) to BGR (CV2) if necessary
                         annotated_img = cv2.cvtColor(annotated_img, cv2.COLOR_RGB2BGR)
                     elif annotated_img.ndim == 2: # Grayscale to BGR if needed by cv2
                          annotated_img = cv2.cvtColor(annotated_img, cv2.COLOR_GRAY2BGR)
                except Exception as e:
                    print(f"Warning: Could not convert annotated image to numpy array. Error: {e}")
                    print("Skipping save for this image due to conversion issue.")
                    return # Exit function if conversion fails

            # Check if the conversion resulted in a valid image array
            if isinstance(annotated_img, np.ndarray) and annotated_img.ndim >= 2:
                 cv2.imwrite(output_path, annotated_img)
                 print(f"Segmented image saved to {output_path}")
            else:
                 print(f"Warning: Annotated image data is not a valid numpy array after processing. Skipping save.")


        else:
            print(f"No objects with masks found in image from URL: {image_url}.")
            # Could add logic here to save the original downloaded image if needed

    else:
        print(f"No results obtained for URL: {image_url}. The URL might be invalid or something went wrong fetching/processing it.")


# --- Script Entry Point ---
if __name__ == "__main__":
    # --- Hardcoded Image URL ---
    # Replace this with the URL of the image you want to segment!
    hardcoded_image_url = "https://ultralytics.com/images/bus.jpg" # Example URL

    if hardcoded_image_url == "REPLACE_THIS_URL":
        print("Error: Please replace 'REPLACE_THIS_URL' with a valid image URL.")
    else:
        # Added a basic check if cv2 is available before calling the function
        # to give a clearer error if opencv-python wasn't installed.
        try:
            import cv2
        except ImportError:
            print("Error: OpenCV (cv2) not found. Please install it using 'pip install opencv-python'")
        else:
            segment_image_from_url(hardcoded_image_url)
