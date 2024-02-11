import json
import os
import socket
import cv2
import numpy as np
import torch


def detect_drones(image_bytes, model):
    # Convert image bytes to a NumPy array and process
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_tensor = torch.tensor(img_rgb).float().permute(2, 0, 1).unsqueeze(0) / 255.0

    with torch.no_grad():
        results = model(img_tensor)

    boxes = results.xyxy[0]
    drones_coords = [
        [box[0].item(), box[1].item(), box[2].item(), box[3].item()]
        for box in boxes
        if box[-1] == 0
    ]

    return drones_coords


def main():
    # Attempt to find the project's root directory based on the location of the current script
    try:
        project_root = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        print("Could not determine the script's directory; '__file__' is undefined.")
        return

    # Path to the model file within the project structure
    model_path = os.path.join(project_root, "models", "15_10_23_colab_v1_best.pt")
    model = torch.load(model_path, map_location=torch.device("cpu"))
    model.eval()

    # Unix socket setup
    socket_path = "/tmp/catch_video_system_v1_unix_socket"
    try:
        os.unlink(socket_path)
    except OSError:
        if os.path.exists(socket_path):
            raise

    server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server_socket.bind(socket_path)
    server_socket.listen(1)
    print("Catch Video System is listening for connections...")

    while True:
        connection, _ = server_socket.accept()
        try:
            image_data = b""
            while True:
                packet = connection.recv(4096)
                if not packet:
                    break
                image_data += packet

            if image_data:
                coords = detect_drones(image_data, model)
                response = json.dumps(coords)
                connection.sendall(response.encode("utf-8"))
        finally:
            connection.close()


if __name__ == "__main__":
    main()
