from typing import Dict

from PIL import Image
from ultralytics import YOLO
from datetime import datetime


class Recognizer:

    def __init__(self, model_path, debug=False) -> None:
        self.debug = debug
        # TODO: export
        # Load a YOLOv8n PyTorch model
        print("export was started")
        model = YOLO(model_path)
        # Export the model to TensorRT format
        model.export(format="engine")
        print("export is done")
    
    def detect_drones(self, frame) -> Dict[str, int]:
        final_result = {
            "xmin": None,
            "ymin": None,
            "xmax": None,
            "ymax": None,
            "conf": 0.0,
        }

        pred_results = self.model([frame])

        drones_coords = pred_results[0].boxes.xyxy
        conf = pred_results[0].boxes.conf

        # xmin, ymin, xmax, ymax = drones_coords[0].tolist()
        # confidence = conf.item()
        if drones_coords is not None and len(drones_coords) > 0:
            xmin, ymin, xmax, ymax = drones_coords[0].tolist()
            confidence = conf.item()
        else:
            xmin, ymin, xmax, ymax = 0, 0, 0, 0
            confidence = 0

        print(
            f"Coordinates: xmin={xmin}, ymin={ymin}, xmax={xmax}, ymax={ymax}, Confidence: {confidence}"
        )

        final_result["xmin"] = xmin
        final_result["ymin"] = ymin
        final_result["xmax"] = xmax
        final_result["ymax"] = ymax
        final_result["conf"] = confidence

        if self.debug:
            im_array = pred_results[0].plot()  # plot a BGR numpy array of predictions
            im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"data/prediction_results/results-{timestamp}.jpg"
            im.save(file_name)

        return final_result