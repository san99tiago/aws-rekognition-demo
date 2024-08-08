# Built-in imports
import io
import json
from typing import Optional, Any

# External imports
import boto3
from botocore.exceptions import ClientError
from aws_lambda_powertools import Logger


logger = Logger(
    service="rekognition-demo",
    log_uncaught_exceptions=True,
    owner="santi-tests",
)


class S3Helper:
    def __init__(self, bucket_name: str, s3_client: Optional[callable] = None) -> None:
        self.bucket_name = bucket_name
        self.s3_client = s3_client or boto3.client("s3")

    def upload_fileobj_to_s3(
        self,
        filename: str,
        data: Any,
    ) -> tuple[bool, str, Any]:
        success = True

        logger.info(f"Starting upload of {filename} to {self.bucket_name}...")
        try:
            self.s3_client.upload_fileobj(data, self.bucket_name, filename)
            logger.info(f"Uploaded {filename} to {self.bucket_name} successfully")
        except ClientError as error:
            success = False
            logger.error(
                "Writing to s3 failed. Bucket:%s, Filename:%s,Error:%s",
                self.bucket_name,
                filename,
                str(error),
            )
            raise error

        return success, filename
