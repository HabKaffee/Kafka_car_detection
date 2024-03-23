from ultralytics import YOLO
import torch

class YOLOv8:
    def __init__(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = self.load_model()

    def load_model(self):
        model = YOLO('yolov8n.pt', task='detection')
        model.fuse()
        return model

    def predict(self, frame):
        res = self.model(frame, conf=0.25)
        return res

    def plot_bboxes(self, results):
        xyxys = []
        confidences = []
        class_ids = []

        for result in results:
            boxes = result.boxes.cpu().numpy()

            xyxys.append(boxes.xyxy)
            confidences.append(boxes.conf)
            class_ids.append(boxes.cls)
        return results[0].plot(), xyxys, confidences, class_ids
