from djitellopy import tello
from numpy import source
import torch
import cv2
from time import sleep
from PIL import Image
me = tello.Tello()
me.connect()

print(me.get_battery())
me.streamon()

#model def
model = torch.hub.load('best.pt', source='local')  # local repo
#model.load_state_dict(torch.load('best.pt'))
#model.load_state_dict(torch.load('load/from/path/model.pth'))


#model = torch.hub.load('experiment1', 'custom', 'experiment1/best.pt', source='local')
#model = torch.hub.load('/Users/robin/Github/yolov5', 'custom', 'pytorch/object-detection/yolov5/experiment1/best.pt', source='local')  # local repo

def yolo(im, size=640):
    g = (size / max(im.size))  # gain
    im = im.resize((int(x * g) for x in im.size), Image.ANTIALIAS)  # resize

    results = model(im)  # inference
    results.render()  # updates results.imgs with boxes and labels
    return Image.fromarray(results.imgs[0])

while True :
    img = me.get_frame_read().frame
    #img = cv2.resize(img, (900, 600))
    img = Image.fromarray(img)
    img = yolo(img)
    #img = img.resize((900, 600), Image.ANTIALIAS)
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imshow('frame', img)
    cv2.waitKey(2)


"""
Source: https://github.com/AK391/yolov5/blob/master/utils/gradio/demo.py
"""

import gradio as gr
import torch
from PIL import Image

# Model
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # force_reload=True to update



inputs = gr.inputs.Image(type='pil', label="Original Image")
outputs = gr.outputs.Image(type="pil", label="Output Image")

title = "YOLOv5"
description = "YOLOv5 demo for object detection. Upload an image or click an example image to use."
article = "<p style='text-align: center'>YOLOv5 is a family of compound-scaled object detection models trained on the COCO dataset, and includes " \
          "simple functionality for Test Time Augmentation (TTA), model ensembling, hyperparameter evolution, " \
          "and export to ONNX, CoreML and TFLite. <a href='https://github.com/ultralytics/yolov5'>Source code</a> |" \
          "<a href='https://apps.apple.com/app/id1452689527'>iOS App</a> | <a href='https://pytorch.org/hub/ultralytics_yolov5'>PyTorch Hub</a></p>"

examples = [['images/pan-fire.jpg'], ['images/fire-basket.jpg']]
gr.Interface(yolo, inputs, outputs, title=title, description=description, article=article, examples=examples).launch(
    debug=True)