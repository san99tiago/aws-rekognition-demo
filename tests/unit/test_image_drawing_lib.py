import os
import pytest
from hashlib import sha256


@pytest.fixture
def rekognition_response_wegner_vogels():
    return {
        "CelebrityFaces": [
            {
                "Urls": ["www.wikidata.org/wiki/Q2536951"],
                "Name": "Werner Vogels",
                "Id": "23iZ1oP",
                "Face": {
                    "BoundingBox": {
                        "Width": 0.14352034032344818,
                        "Height": 0.27111920714378357,
                        "Left": 0.41607487201690674,
                        "Top": 0.1123516783118248,
                    },
                    "Confidence": 99.997802734375,
                    "Landmarks": [
                        {
                            "Type": "eyeLeft",
                            "X": 0.4609915614128113,
                            "Y": 0.21723824739456177,
                        },
                        {
                            "Type": "mouthRight",
                            "X": 0.5215809941291809,
                            "Y": 0.3037998080253601,
                        },
                        {
                            "Type": "nose",
                            "X": 0.49727413058280945,
                            "Y": 0.25252798199653625,
                        },
                        {
                            "Type": "eyeRight",
                            "X": 0.5220686197280884,
                            "Y": 0.211320161819458,
                        },
                        {
                            "Type": "mouthLeft",
                            "X": 0.4706871211528778,
                            "Y": 0.3088351786136627,
                        },
                    ],
                    "Pose": {
                        "Roll": -2.8998947143554688,
                        "Yaw": 3.560572862625122,
                        "Pitch": 17.836177825927734,
                    },
                    "Quality": {
                        "Brightness": 88.97479248046875,
                        "Sharpness": 78.64350128173828,
                    },
                    "Emotions": [
                        {"Type": "CALM", "Confidence": 98.49304962158203},
                        {"Type": "CONFUSED", "Confidence": 0.632191002368927},
                        {"Type": "SAD", "Confidence": 0.20497243106365204},
                        {"Type": "SURPRISED", "Confidence": 0.18563257157802582},
                        {"Type": "HAPPY", "Confidence": 0.17765991389751434},
                        {"Type": "DISGUSTED", "Confidence": 0.14531922340393066},
                        {"Type": "ANGRY", "Confidence": 0.13370108604431152},
                        {"Type": "FEAR", "Confidence": 0.027466440573334694},
                    ],
                    "Smile": {"Value": False, "Confidence": 97.53596496582031},
                },
                "MatchConfidence": 99.83985137939453,
                "KnownGender": {"Type": "Male"},
            }
        ],
        "UnrecognizedFaces": [],
        "ResponseMetadata": {
            "RequestId": "ac4fd61d-8139-4c9d-9889-ff294314b0f3",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "x-amzn-requestid": "ac4fd61d-8139-4c9d-9889-ff294314b0f3",
                "content-type": "application/x-amz-json-1.1",
                "content-length": "1330",
                "date": "Thu, 08 Aug 2024 20:35:27 GMT",
            },
            "RetryAttempts": 0,
        },
    }


@pytest.fixture
def werner_vogels_image_path():
    PATH_IMAGES_FOLDER = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data",
        "famous",
    )
    return os.path.join(PATH_IMAGES_FOLDER, "werner_vogels.png")


@pytest.fixture
def expected_werner_vogels_image_with_drawing_sha256():
    return "111efe7d60548f6841fddcaf330fdfe2bdd454921159589164dd216ddead9ba2"


@pytest.fixture
def output_result_image_path():
    PATH_IMAGES_FOLDER = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data",
        "famous",
    )
    return os.path.join(PATH_IMAGES_FOLDER, "test_output_result.png")


def test_draw_faces_in_memory(
    rekognition_response_wegner_vogels: str,
    werner_vogels_image_path: str,
    output_result_image_path: str,
):
    from image_detect_famous.image_drawing_lib import ImageDrawing

    image_drawing = ImageDrawing(
        image_path=werner_vogels_image_path,
        rekognition_detect_face_response=rekognition_response_wegner_vogels,
        result_demo_output_path=output_result_image_path,
    )

    image_drawing.draw_faces()

    # Check if the image was loaded
    assert image_drawing.image is not None


def test_draw_faces_save_file(
    rekognition_response_wegner_vogels: str,
    werner_vogels_image_path: str,
    output_result_image_path: str,
    expected_werner_vogels_image_with_drawing_sha256: str,
):
    from image_detect_famous.image_drawing_lib import ImageDrawing

    image_drawing = ImageDrawing(
        image_path=werner_vogels_image_path,
        rekognition_detect_face_response=rekognition_response_wegner_vogels,
        result_demo_output_path=output_result_image_path,
    )

    image_drawing.draw_faces()
    image_drawing.save_image()

    # Check if the file was created
    assert os.path.exists(output_result_image_path)

    # Generate SHA256 hash of the saved image file
    with open(output_result_image_path, "rb") as image_file:
        file_hash = sha256(image_file.read()).hexdigest()

    # Check if the generated hash matches the expected hash
    assert (
        file_hash == expected_werner_vogels_image_with_drawing_sha256
    ), f"SHA256 hash does not match! Expected {expected_werner_vogels_image_with_drawing_sha256}, got {file_hash}"

    # Clean up
    os.remove(output_result_image_path)
