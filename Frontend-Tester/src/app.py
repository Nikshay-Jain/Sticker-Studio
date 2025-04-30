# app.py
import os, subprocess
import streamlit as st

from main import setup_environment, setup_logging, load_classifier_model, process_sticker_from_image, process_sticker_from_text

# Set up environment and directories
setup_environment()

# Set up logging
log_filename = setup_logging()

# Load the classifier model
# The classifier might be used differently or not at all for generated images,
# but we load it here as it's part of the setup.
is_normal_classifier = load_classifier_model()

subprocess.run(["python3", "tracking/app.py"])

# Streamlit UI
# --- Theme-Aware Styling ---
st.markdown(
    """
    <style>
    :root, html, body, .stApp {
        background-color: black !important;
    }
    .stRadio > div {
        flex-direction: row !important;
        justify-content: center;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        border-radius: 8px;
        padding: 0.75em 1.5em;
        margin-top: 1em;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .stTextInput > div > input {
        font-size: 16px;
        border-radius: 8px;
    }
    .stColorPicker > div {
        padding-top: 0.5em;
    }
    @media (prefers-color-scheme: dark) {
        .stMarkdown h3 {
            color: #f0f0f0;
        }
    }
    @media (prefers-color-scheme: light) {
        .stMarkdown h3 {
            color: #333333;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Monitoring Dashboard Links ---
with st.sidebar:
    st.markdown("### 🔍 Monitoring")
    st.markdown("[📊 Prometheus Dashboard](http://localhost:9090)", unsafe_allow_html=True)
    st.markdown("[📊 Prometheus Client](http://localhost:18000)", unsafe_allow_html=True)
    st.markdown("[📈 Grafana Dashboard](http://localhost:3000)", unsafe_allow_html=True)
st.title("Sticker Studio 🎨")

# --- Input Method Selection ---
# Provide two options for the user: upload an image or generate from text.
option = st.radio("Choose input method:", ("Upload image directly", "Enter text for Gen-AI images"))

uploaded_file = None
text_for_image = None    # Variable to hold text input for image generation

# --- Conditional Input Fields ---
# Display input fields based on the selected option.
if option == "Upload image directly":
    # Input for image upload
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
elif option == "Enter text for Gen-AI images":
    # Input for text-to-image generation
    text_for_image = st.text_input("Enter text to generate an image:")

# --- Common Inputs for Sticker Generation ---
# These inputs are needed regardless of the image source.
text_input = st.text_input("Enter Caption for the sticker:")
color = st.color_picker("Pick a Text Color", "#FFFFFF")

# Font options (remains the same)
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

# Load selected font (remains the same)
font_url = font_options[selected_font]
st.markdown(f'<link href="{font_url}" rel="stylesheet">', unsafe_allow_html=True)

# Font preview (remains the same)
st.markdown(
    f"""
    <p style="font-family: '{selected_font}', cursive; font-size: 28px; color: {color}; text-align: center;">
    {text_input if text_input else "Your Text Here"}
    </p>
    """,
    unsafe_allow_html=True
)

# --- Generate Sticker Button Logic ---
# Process based on the selected input method and required inputs.
if st.button("Generate Sticker"):
    output_path = None

    # Check if required inputs are provided based on the selected option
    if option == "Upload image directly":
        if uploaded_file and text_input:
            # Call the function to process uploaded image
            output_path = process_sticker_from_image(
                uploaded_file,
                text_input,
                color,
                selected_font,
                font_files,
                is_normal_classifier,
                log_filename
            )
        elif not uploaded_file:
            st.warning("Please upload an image.")
        elif not text_input:
            st.warning("Please enter text for the sticker caption.")

    elif option == "Enter text for Gen-AI images":
        if text_for_image and text_input:
            # Call the function to process text for image generation
            output_path = process_sticker_from_text(
                text_for_image, # Pass the text for image generation
                text_input,     # Pass the text for the sticker caption
                color,
                selected_font,
                font_files,
                log_filename
            )
        elif not text_for_image:
            st.warning("Please enter text for image generation.")
        elif not text_input:
            st.warning("Please enter text for the sticker caption.")

    # --- Display and Download Sticker ---
    # This part executes if an output_path was successfully returned.
    if output_path and os.path.exists(output_path):
        st.success("Sticker generated successfully! 🎉")
        st.image(output_path, caption="Generated Sticker", use_container_width=True)
        with open(output_path, "rb") as file:
            st.download_button(
                label="Download Sticker",
                data=file,
                file_name="sticker.webp",
                mime="image/webp"
            )
    elif output_path is None:
         # Display an error if processing failed and output_path is None
         st.error("Failed to generate sticker. Please check your inputs and try again.")