# Built-in imports
import os

# External imports
import streamlit as st
from aws_lambda_powertools import Logger

# Own imports
import image_detect_famous_lib as face_detect_lib
import image_drawing_lib as image_drawing_lib
from s3_helper import S3Helper
from enums import S3KeyPath


# Environment Variables
S3_BUCKET = os.environ["S3_BUCKET"]

# Logger
logger = Logger(
    service="rekognition-demo",
    log_uncaught_exceptions=True,
    owner="santi-tests",
)

# Global path configurations
PATH_TO_IMAGES_FOLDER = os.path.join(
    os.path.dirname(__file__),
    "images",
)
DEFAULT_IMAGE_PATH = os.path.join(PATH_TO_IMAGES_FOLDER, "famous", "photo-01.png")
TEMP_INPUT_PATH = os.path.join(PATH_TO_IMAGES_FOLDER, "processing", "input.png")
TEMP_OUTPUT_PATH = os.path.join(PATH_TO_IMAGES_FOLDER, "processing", "output.png")

# Initialize the S3 Helper
s3_helper = S3Helper(S3_BUCKET)

# General Streamlit configurations
st.set_page_config(layout="wide", page_title="Detect Famous People")
st.title("Detect Famous People")
col1, col2, col3 = st.columns([2, 1, 2])

with col1:
    # Obtain image from user's input
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg"])

    if uploaded_file:
        # Load the image preview from the uploaded file
        uploaded_image_preview = face_detect_lib.get_bytesio_from_bytes(
            uploaded_file.getvalue()
        )
        st.image(uploaded_image_preview)
    else:
        # Load the image preview from the default file
        st.image(DEFAULT_IMAGE_PATH)

with col2:
    st.subheader("Detect Famous")
    st.write("Click the button below to detect famous people in the image.")
    generate_button = st.button("Detect", type="primary")


with col3:
    st.subheader("Result")

    if generate_button:
        logger.info("Starting the generation process...")
        if uploaded_file:
            image_bytes = uploaded_file.getvalue()

            # Upload the image to S3
            s3_helper.upload_fileobj_to_s3(
                filename=S3KeyPath.UPLOADED_IMAGE.value,
                data=uploaded_file,
            )
        else:
            image_bytes = face_detect_lib.get_bytes_from_file(DEFAULT_IMAGE_PATH)

            # Upload the image to S3
            with open(DEFAULT_IMAGE_PATH, "rb") as data:
                s3_helper.upload_fileobj_to_s3(
                    filename=S3KeyPath.UPLOADED_IMAGE.value,
                    data=data,
                )

        # Save the image to a local file for processing
        with open(TEMP_INPUT_PATH, "wb") as file:
            file.write(image_bytes)

        with st.spinner("Drawing..."):
            logger.info("Detecting famous people in the image...")
            result = face_detect_lib.recognize_celebrities(
                s3_bucket_name=S3_BUCKET, image_key=S3KeyPath.UPLOADED_IMAGE.value
            )
            logger.info("Famous people detection finished!")
            logger.info(result, message_details="Result")

            image_drawing = image_drawing_lib.ImageDrawing(
                image_path=TEMP_INPUT_PATH,
                rekognition_detect_face_response=result,
                result_demo_output_path=TEMP_OUTPUT_PATH,
            )
            image_drawing.draw_faces()
            image_drawing.save_image()
            st.image(TEMP_OUTPUT_PATH)
            st.write(result)
