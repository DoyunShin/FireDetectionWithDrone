from djitellopy import tello
import cv2
from time import sleep
import logging

me = tello.Tello()
me.LOGGER.setLevel(logging.DEBUG)
# debug mode
print("CONN")
me.connect()

print(me.get_battery())
me.streamon()

while True:
    img = me.get_frame_read().frame
    cv2.imshow("IMG", img)
    cv2.waitKey(2)