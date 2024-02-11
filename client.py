import socket
import os


def send_image(image_path, socket_path="/tmp/catch_video_system_v1_unix_socket"):
    """
    Sends an image to a server via a Unix domain socket and prints the server's response.

    Args:
    - image_path: The filesystem path to the image file to send.
    - socket_path: The filesystem path to the Unix domain socket for communication.
    """
    client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        client_socket.connect(socket_path)

        with open(image_path, "rb") as image_file:
            client_socket.sendall(image_file.read())

        # Wait for and print the server's response
        response = client_socket.recv(4096)
        print("Received:", response.decode("utf-8"))
    finally:
        client_socket.close()


def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    image_name = "quadcopter_1.jpeg"
    image_path = os.path.join(project_root, "data", "test_images", image_name)

    # Call the function to send the image
    send_image(image_path)


if __name__ == "__main__":
    main()
