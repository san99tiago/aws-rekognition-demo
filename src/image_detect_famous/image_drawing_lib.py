import os
from PIL import Image, ImageDraw, ImageFont

# Global path configurations
PATH_IMAGES_FOLDER = os.path.join(
    os.path.dirname(__file__),
    "images",
)
result_demo_input_path = os.path.join(PATH_IMAGES_FOLDER, "results", "input.png")
result_demo_output_path = os.path.join(PATH_IMAGES_FOLDER, "results", "output.png")


class ImageDrawing:
    """Class to draw faces on an image"""

    def __init__(
        self,
        image_path: str,
        rekognition_detect_face_response: dict,
        result_demo_output_path: str,
    ):
        """
        :param image_path: Path to the image file in the local system.
        :param rekognition_detect_face_response: Response from AWS Rekognition DetectFaces API.
            Should contain the CelebrityFaces key.
        :param result_demo_output_path: Path to save the modified image.
        """
        self.image = Image.open(image_path)
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.load_default(size=24)
        self.rekognition_detect_face_response = rekognition_detect_face_response
        self.result_demo_output_path = result_demo_output_path

    def draw_faces(self):
        """
        Draw faces on the image and save it back to the same file.
        """
        for match in self.rekognition_detect_face_response["CelebrityFaces"]:
            # Debug prints
            print("Bounding Box:", match["Face"]["BoundingBox"])
            print("Image Size:", self.image.size)
            print("The face identified is:", match["Name"])

            # Draw green square around recognized face
            box = match["Face"]["BoundingBox"]
            img_width, img_height = self.image.size
            left = img_width * box["Left"]
            top = img_height * box["Top"]
            width = img_width * box["Width"]
            height = img_height * box["Height"]
            print("Drawing Rectangle:", left, top, left + width, top + height)
            self.draw.rectangle(
                [left, top, left + width, top + height], outline="red", width=5
            )

            # Display name at the bottom
            text = match["Name"]
            f = self.draw.textlength(text, self.font)
            print("Text Position:", left, top + height)
            self.draw.text((left, top + height), text, fill="red", font=self.font)

    def save_image(self):
        """
        Save the modified image back to the same file.
        """
        # Save the modified image back to the same file
        self.image.save(self.result_demo_output_path)
