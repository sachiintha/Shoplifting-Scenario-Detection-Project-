#emotion_model/
import cv2
import numpy as np

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.shoplifting_detected = False
        self.people_count = 0

        # Load YOLO model for object detection
        self.net = cv2.dnn.readNet("emotion_model/yolov3.weights", "emotion_model/yolov3.cfg")  # Replace with actual paths
        self.classes = []  # Load class names from a file (e.g., coco.names)
        with open("emotion_model/coco.names", "r") as f:
            self.classes = f.read().strip().split("\n")

    def __del__(self):
        self.video.release()

    def detect_shoplifting(self):
        # Reset the shoplifting_detected flag
        self.shoplifting_detected = False

        _, fr = self.video.read()

        # Implement your YOLO-based object detection logic here
        blob = cv2.dnn.blobFromImage(fr, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.net.getUnconnectedOutLayersNames())

        class_ids = []
        confidences = []
        boxes = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.85:  # Adjust confidence threshold
                    # Example: Check if the class corresponds to a mobile phone
                    if self.classes[class_id] == 'cell phone':  # Replace with the correct class name
                        self.shoplifting_detected = True
                        break  # No need to continue checking other detections

    def get_frame(self):
        _, fr = self.video.read()

        # Call the detect_shoplifting function
        self.detect_shoplifting()

        # People counting
        gray_fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        faces = cv2.CascadeClassifier('haarcascade_frontalface_default.xml').detectMultiScale(gray_fr, 1.3, 5)
        self.people_count = len(faces)

        # Draw people count on the frame
        cv2.putText(fr, f"People Count: {self.people_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Draw potential shoplifting warning on the frame
        if self.shoplifting_detected:
            cv2.putText(fr, "Potential Shoplifting!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        _, jpeg = cv2.imencode('.jpg', fr)
        return jpeg.tobytes()
