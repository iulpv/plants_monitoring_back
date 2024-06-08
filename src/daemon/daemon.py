import time

import cv2
import requests

from src.api.settings import Settings

settings = Settings()
url = settings.host + ':' + str(settings.port)
capture_number = 0

for i in range(10):
    capture = cv2.VideoCapture(i)
    if capture.isOpened():
        capture.release()
        capture_number = i
        break

try:
    while True:
        capture = cv2.VideoCapture(capture_number)
        if not capture.isOpened():
            continue
        else:
            ret, frame = capture.read()
            if ret and frame.size > 0:
                _, image_data = cv2.imencode('.jpg', frame)
                files = {'file': ('image.jpg', image_data.tobytes(), 'image/jpeg')}
                response = requests.post(f'http://{url}/predict/camera-photo', files=files)
            capture.release()

        time.sleep(10)
except KeyboardInterrupt:
    cv2.destroyAllWindows()
    exit()
