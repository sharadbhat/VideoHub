import cv2
import numpy as np
import os

def save_image(video_ID):
    """
    - Saves the first frame of the video as an image.
    """
    frame_num = 0
    cap = cv2.VideoCapture('static/videos/{}.mp4'.format(video_ID))
    while True:
        frame_num += 1
        ret, frame = cap.read()
        if frame_num == 115: # 5 seconds
            name = 'static/images/{}.jpg'.format(video_ID)
            cv2.imwrite(name, frame)
            cap.release()
            cv2.destroyAllWindows()
            break
