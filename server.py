import io
import json
import os
import socket
from datetime import datetime

from PIL import Image
from ultralytics import YOLO


def detect_drones(image, model):
    final_result = {
        "xmin": None,
        "ymin": None,
        "xmax": None,
        "ymax": None,
        "conf": 0.0,
    }

    pred_results = model([image])

    drones_coords = pred_results[0].boxes.xyxy
    conf = pred_results[0].boxes.conf

    xmin, ymin, xmax, ymax = drones_coords[0].tolist()
    confidence = conf.item()

    print(
        f"Coordinates: xmin={xmin}, ymin={ymin}, xmax={xmax}, ymax={ymax}, Confidence: {confidence}"
    )

    final_result["xmin"] = xmin
    final_result["ymin"] = ymin
    final_result["xmax"] = xmax
    final_result["ymax"] = ymax
    final_result["conf"] = confidence

    im_array = pred_results[0].plot()  # plot a BGR numpy array of predictions
    im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"data/prediction_results/results-{timestamp}.jpg"
    im.save(file_name)

    return final_result


def main():
    # Attempt to find the project's root directory based on the location of the current script
    try:
        project_root = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        print("Could not determine the script's directory; '__file__' is undefined.")
        return

    model_path = os.path.join(project_root, "models", "15_10_23_colab_v1_best.pt")
    model = YOLO(model_path)

    socket_path = "/tmp/catch_video_system_v1_unix_socket"
    if os.path.exists(socket_path):
        os.unlink(socket_path)

    server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server_socket.bind(socket_path)
    server_socket.listen(1)
    print("Catch Video System is listening for connections...")

    while True:
        connection, _ = server_socket.accept()
        try:
            # First, read the size of the image data
            header = connection.recv(64)
            if not header:
                print("No header received")
                continue
            data_size = int(header.decode("utf-8").strip())
            image_data = b""

            # Then, read the image data
            while len(image_data) < data_size:
                packet = connection.recv(4096)
                if not packet:
                    break
                image_data += packet

            if image_data:
                print("Image data was received. Start processing...")
                image = Image.open(io.BytesIO(image_data))
                coords = detect_drones(image, model)
                response = json.dumps(coords)
                connection.sendall(response.encode("utf-8"))
                print("Image was processed successfully. Listening for next one...")
        finally:
            connection.close()


if __name__ == "__main__":
    main()
