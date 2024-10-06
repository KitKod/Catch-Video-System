import torch  # NOTE: Don't delete this line. It is important! Import torch early than Recognizer
import os
# os.environ["OMP_NUM_THREADS"] = "1" May help to solve issue with TLS
import sys
sys.path.append('/usr/lib/python3.8/site-packages')
print(sys.path)

import cv2
import nanocamera as nano
from recognizer import Recognizer

if __name__ == '__main__':
    # Attempt to find the project's root directory based on the location of the current script
    try:
        project_root = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        print("Could not determine the script's directory; '__file__' is undefined.")
        sys.exit(1)

    model_path = os.path.join(project_root, "models", "15_10_23_colab_v1_best.pt")
    recognizer = Recognizer(model_path, True)

    # Create the Camera instance
    camera = nano.Camera(camera_type=1, device_id=0, flip=2, width=640, height=480, fps=30)
    print('CSI Camera ready? - ', camera.isReady())

    while camera.isReady():
        try:
            # read the camera image
            frame = camera.read()
            # display the frame
            cv2.imshow("Video Frame", frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            
            print(recognizer.detect_drones(frame))

        except KeyboardInterrupt:
            break

    # close the camera instance
    camera.release()
    # remove camera object
    del camera