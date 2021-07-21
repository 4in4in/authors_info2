import cv2
# import numpy as np
import imageio

class FaceDetector:
    prototxt_path = './src/utils/model_data/deploy.prototxt'
    caffemodel_path = './src/utils/model_data/weights.caffemodel'

    model = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)

    @classmethod
    def is_image_contains_face(cls, img_bytes):
        try:
            img = imageio.imread(img_bytes)
        except:
            return False
        cv2_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        blob = cv2.dnn.blobFromImage(cv2.resize(cv2_img, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
        cls.model.setInput(blob)
        detections = cls.model.forward()
        min_confidence = 0.7
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > min_confidence:
                return True
        return False

        