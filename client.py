import os
import socket


def send_image(image_path, socket_path="/tmp/catch_video_system_v1_unix_socket"):
    client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        client_socket.connect(socket_path)

        # Read the image data
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

        # Send the size of the image data as a 64-byte header
        header = f"{len(image_data):<64}".encode("utf-8")
        client_socket.sendall(header + image_data)
        print("The image was sent")

        # Wait for and print the server's response
        print("Waiting for server response...")
        response = client_socket.recv(4096)
        print("Received:", response.decode("utf-8"))
    finally:
        client_socket.close()


def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    image_name = "quadcopter_1.jpeg"
    image_path = os.path.join(project_root, "data", "test_images", image_name)
    send_image(image_path)


if __name__ == "__main__":
    main()
