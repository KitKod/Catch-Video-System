import sys
sys.path.append('/usr/lib/python3.8/site-packages')

import socket
import nanocamera as nano

import cv2

def send_image(image, socket_path="/tmp/catch_video_system_v1_unix_socket"):
    client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        client_socket.connect(socket_path)

        # Encode the frame as JPEG
        success, encoded_image = cv2.imencode('.jpg', image)

        if not success:
            print("Failed to encode the image.")
            return

        image_data = encoded_image.tobytes()

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
    camera = nano.Camera(camera_type=1, device_id=0, flip=2, width=640, height=480, fps=30)
    print('CSI Camera ready? - ', camera.isReady())

    while camera.isReady():
        try:
            # read the camera image
            frame = camera.read()
            send_image(frame)
            # display the frame
            cv2.imshow("Video Frame", frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        except KeyboardInterrupt:
            break

    # close the camera instance
    camera.release()
    # remove camera object
    del camera


if __name__ == "__main__":
    main()
