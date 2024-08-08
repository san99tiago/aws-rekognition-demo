# Enum for the S3 key path
from enum import Enum


class S3KeyPath(Enum):
    UPLOADED_IMAGE = "uploaded_image.png"
    RESULT_IMAGE = "result_image.png"
