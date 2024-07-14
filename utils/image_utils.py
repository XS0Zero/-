import base64
import numpy as np
import cv2


def png_to_base64(file_path):
    with open(file_path, "rb") as file:
        base64_data = base64.b64encode(file.read()).decode("utf-8")
    return base64_data


def base64_to_image(base64_data, output_path):
    # Convert base64 to bytes
    base64_data = base64_data.encode('utf-8')
    image_data = base64.b64decode(base64_data)

    # Convert bytes to numpy array
    image_array = np.frombuffer(image_data, np.uint8)

    # Convert numpy array to opencv image
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    # Save image to file
    cv2.imwrite(output_path, image)


if __name__ == "__main__":
    file_path = "../window_capture.png"
    base64_data = png_to_base64(file_path)

    print(base64_data)
    output_path = "../output_image.png"

    base64_to_image(base64_data, output_path)
