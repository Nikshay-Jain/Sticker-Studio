import streamlit as st
import os, atexit, logging
from datetime import datetime

from segmentor_model import segmentor
from to_ghibli import theme_convertor
from sticker_generator import generate_sticker
from ghibli_normal_classifier import predict_with_resnet

from tensorflow.keras.models import load_model

# Ensure necessary directories exist
UPLOAD_DIR = r"C:\Users\niksh\Desktop\Ghibli-Sticker-Studio\uploads"
OUTPUT_DIR = "stickers"
FONTS_DIR = "fonts"
LOG_DIR = "logs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FONTS_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
log_filename = os.path.join(LOG_DIR, f"studio_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logging.info("=== AI Sticker Studio started ===")

def log_exit():
    global _exit_logged
    if not _exit_logged:
        logging.info("=== AI Sticker Studio closed ===")
        _exit_logged = True

_exit_logged = False
atexit.register(log_exit)

# Load classifier model
try:
    resnet_model_path = 'models\Ghibli-normal-classifier\Resnet_ghibli_normal.h5'
    resnet_model = load_model(resnet_model_path)
    logging.info(f"ResNet model loaded from: {resnet_model_path}")
except FileNotFoundError:
    resnet_model = None
    logging.warning(f"ResNet model not found at: {resnet_model_path}. 'Normal' prediction based theming will be skipped.")
except Exception as e:
    resnet_model = None
    logging.error(f"Error loading ResNet model: {e}. 'Normal' prediction based theming will be skipped.")

# Streamlit UI
st.title("AI Sticker Studio 🎨")

# Take inputs
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
text_input = st.text_input("Enter Caption for the sticker:")
theme = st.selectbox("Choose Theme:", ["Original", "Ghibli"])
color = st.color_picker("Pick a Text Color", "#FFFFFF")

# Font options
font_options = {
    "Bangers": "https://fonts.googleapis.com/css2?family=Bangers&display=swap",
    "Lobster": "https://fonts.googleapis.com/css2?family=Lobster&display=swap",
    "Pacifico": "https://fonts.googleapis.com/css2?family=Pacifico&display=swap",
    "Anton": "https://fonts.googleapis.com/css2?family=Anton&display=swap"
}

font_files = {
    "Bangers": "Bangers-Regular",
    "Lobster": "Lobster-Regular",
    "Pacifico": "Pacifico-Regular",
    "Anton": "Anton-Regular"
}

st.markdown("### Choose Font Style:")
selected_font = st.radio("Select Font Style:", list(font_options.keys()), horizontal=True)

# Load the selected font for UI display
font_url = font_options[selected_font]
st.markdown(f'<link href="{font_url}" rel="stylesheet">', unsafe_allow_html=True)

# Show the font preview
st.markdown(
    f"""
    <p style="font-family: '{selected_font}', cursive; font-size: 28px; color: {color}; text-align: center;">
    {text_input if text_input else "Your Text Here"}
    </p>
    """,
    unsafe_allow_html=True
)

# Generate Button
if st.button("Generate Sticker"):
    if uploaded_file and text_input:
        try:
            # Save uploaded image
            file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            logging.info(f"Uploaded file saved: {file_path}")

            # Get correct font filename
            font_filename = font_files[selected_font]

            # Change theme to ghibli if selected
            if resnet_model is not None and predict_with_resnet(file_path, resnet_model, log_filename):
                logging.info("Applying Ghibli theme...")
                themed_img_path = os.path.join(OUTPUT_DIR, f"themed_{uploaded_file.name}")
                if not os.path.exists(themed_img_path):
                    themed_img_path = theme_convertor(file_path, log_filename)
                else:
                    logging.info(f"Theme already applied: {themed_img_path}")
            else:
                themed_img_path = file_path

            # Process the image
            logging.info(f"Segmenting image: {file_path}")
            seg_img_path = segmentor(themed_img_path, log_filename)

            logging.info(f"Generating sticker with caption: {text_input}, theme: {theme}, color: {color}")
            output_path = generate_sticker(seg_img_path, text_input, color, font_filename, log_filename)

            # Ensure file exists before displaying
            if os.path.exists(output_path):
                st.success("Sticker generated successfully! 🎉")
                st.image(output_path, caption="Generated Sticker", use_container_width=True)
                logging.info(f"Sticker successfully generated: {output_path}")

                # Download button
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="Download Sticker",
                        data=file,
                        file_name="sticker.png",
                        mime="image/png"
                    )
            else:
                st.error("Failed to generate sticker. Please try again.")
                logging.error("Sticker generation failed.")
        except Exception as e:
            st.error("An error occurred while generating the sticker.")
            logging.exception(f"Error in sticker generation: {e}")
    else:
        st.warning("Please upload an image and enter text.")
        logging.warning("Attempted to generate sticker without both image and text.")