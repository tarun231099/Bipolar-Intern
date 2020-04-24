import cv2
import numpy as np

def model():
  cfg_path = 'C:\\Users\\Asus\\Documents\\GitHub\\Bipolar-Intern\\yolov3-spp.cfg'
  weights_path = 'C:\\Users\\Asus\\Documents\\GitHub\\Ciphense\\yolov3-spp.weights'
  net = cv2.dnn.readNet(weights_path , cfg_path)
  return net 

def predict(img,net):
  if img.all() == None:
    print("Image Not Found")
  else:
    classes = []
    with open("coco.names", "r") as f:   #classes available in yolo
     classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    #reading the image
    #img = cv2.imread("dogwalk.jpg")
    img = cv2.resize(img, None, fx=0.5, fy=0.5)   #we resize the image for faster calculation
    height, width, channels = img.shape

    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False) #yolo takes three sizes. 320 x 320,416 x 416 ,608 x 608
    net.setInput(blob)
    outs = net.forward(output_layers)
    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
      for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
          center_x = int(detection[0] * width)
          center_y = int(detection[1] * height)
          w = int(detection[2] * width)
          h = int(detection[3] * height)
          x = int(center_x - w / 2)
          y = int(center_y - h / 2)
          boxes.append([x, y, w, h])
          confidences.append(float(confidence))
          class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)   #mean of all boxes (default)
    resclass = []  #to store the resultant classes
    #font = cv2.FONT_HERSHEY_TRIPLEX
    for i in range(len(boxes)):
      if i in indexes:
    #    x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        resclass.append(label)
    return resclass