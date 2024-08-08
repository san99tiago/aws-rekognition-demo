# Built-in imports
import base64
from io import BytesIO

# External imports
import boto3

rekognition_client = boto3.client("rekognition")


# get a BytesIO object from file bytes
def get_bytesio_from_bytes(image_bytes):
    image_io = BytesIO(image_bytes)
    return image_io


# get a base64-encoded string from file bytes
def get_base64_from_bytes(image_bytes):
    resized_io = get_bytesio_from_bytes(image_bytes)
    img_str = base64.b64encode(resized_io.getvalue()).decode("utf-8")
    return img_str


# load the bytes from a file on disk
def get_bytes_from_file(file_path):
    with open(file_path, "rb") as image_file:
        file_bytes = image_file.read()
    return file_bytes


def detect_faces(s3_bucket_name: str, image_key: str):
    """
    Detect faces in an image.
    """
    result = rekognition_client.detect_faces(
        Image={
            "S3Object": {
                "Bucket": s3_bucket_name,
                "Name": image_key,
            },
        },
    )
    return result


def recognize_celebrities(s3_bucket_name: str, image_key: str):
    """
    Recognize celebrities in an image.
    """
    result = rekognition_client.recognize_celebrities(
        Image={
            "S3Object": {
                "Bucket": s3_bucket_name,
                "Name": image_key,
            },
        },
    )
    return result
