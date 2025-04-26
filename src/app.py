import os
import streamlit as st
from main import setup_environment, setup_logging, load_classifier_model, process_sticker

# Set up environment and directories
setup_environment()

# Set up logging
log_filename = setup_logging()

# Load the classifier model
is_normal_classifier = load_classifier_model()

# Streamlit UI
st.title("Ghibli Sticker Studio 🎨")

# Inputs
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
text_input = st.text_input("Enter Caption for the sticker:")
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

# Load selected font
font_url = font_options[selected_font]
st.markdown(f'<link href="{font_url}" rel="stylesheet">', unsafe_allow_html=True)

# Font preview
st.markdown(
    f"""
    <p style="font-family: '{selected_font}', cursive; font-size: 28px; color: {color}; text-align: center;">
    {text_input if text_input else "Your Text Here"}
    </p>
    """,
    unsafe_allow_html=True
)

# Generate Sticker
if st.button("Generate Sticker"):
    if uploaded_file and text_input:
        output_path = process_sticker(
            uploaded_file,
            text_input,
            color,
            selected_font,
            font_files,
            is_normal_classifier,
            log_filename
        )

        if output_path and os.path.exists(output_path):
            st.success("Sticker generated successfully! 🎉")
            st.image(output_path, caption="Generated Sticker", use_container_width=True)
            with open(output_path, "rb") as file:
                st.download_button(
                    label="Download Sticker",
                    data=file,
                    file_name="sticker.png",
                    mime="image/png"
                )
        else:
            st.error("Failed to generate sticker. Please try again.")
    else:
        st.warning("Please upload an image and enter text.")