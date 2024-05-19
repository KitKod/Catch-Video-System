import cv2

print(cv2.__file__)
print(cv2.__version__)


def __usb_pipeline(device_name="/dev/video0"):
    return ('v4l2src device=%s ! '
            'video/x-raw, '
            'width=(int)%d, height=(int)%d, '
            'format=(string)YUY2, framerate=(fraction)%d/1 ! '
            'videoconvert ! '
            'video/x-raw, format=BGR ! '
            'appsink' % (device_name, 640, 480, 30))

# Define the GStreamer pipeline
pipeline = (
    "v4l2src device=/dev/video0 ! "
    "video/x-raw, width=160, height=120, format=YUY2, framerate=30/1 ! "
    "videoconvert ! "
    "video/x-raw, format=BGR ! appsink"
)

# Open the video capture with the GStreamer pipeline
cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
# cap = cv2.VideoCapture(__usb_pipeline(), cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("Error: Unable to open the camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to read frame")
        break

    cv2.imshow("Video Frame", frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()