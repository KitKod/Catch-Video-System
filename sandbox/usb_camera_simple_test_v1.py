import sys
sys.path.append('/usr/lib/python3.8/site-packages')
print(sys.path)


import cv2



print(cv2.__file__)
print(cv2.__version__)


#from nanocamera.NanoCam import Camera
import nanocamera as nano

if __name__ == '__main__':
    # Create the Camera instance
    camera = nano.Camera(camera_type=1, device_id=0, flip=2, width=640, height=480, fps=30, debug=True, enforce_fps=True)
    print('CSI Camera ready? - ', camera.isReady())
    while camera.isReady():
        try:
            # read the camera image
            frame = camera.read()
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

