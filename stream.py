import supervision as sv
import cv2
import time
import argparse
from ultralytics import YOLO
import matplotlib.pyplot as plt

import os
import PyQt5
from pathlib import Path

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.fspath(
    Path(PyQt5.__file__).resolve().parent / "Qt5" / "plugins"
)

class ObjectDetection:
    def __init__(self, source: str, target: str, confidence: float, weights: str, width: 1280, height: 960):
        self.target = target
        self.confidence = confidence        
        self.annotator = sv.BoundingBoxAnnotator()
        self.frame_count = 0
        if source.isnumeric():
            self.source = int(source)
            self.width = width
            self.height = height
            self.fps = 20
            self.video_info = sv.VideoInfo(width=self.width, height=self.height, fps=self.fps)
        else:
            self.source = source
            self.video_info = sv.VideoInfo.from_video_path(self.source)
            self.width = self.video_info.width
            self.height = self.video_info.height
            self.fps = self.video_info.fps
        
        self.tracker = sv.ByteTrack()
        self.model = YOLO(weights)
        self.label_annotator = sv.LabelAnnotator()       
    
    def display_fps(self, frame):
        self.end_time = time.time()
        fps = self.frame_count / (self.end_time - self.start_time)
        
        text = f'FPS: {int(fps)}'
        cv2.putText(frame, text, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        
        self.start_time = time.time()
        self.frame_count = 0
    
    def display_time(self, frame):
        current_time = time.time()
        
        text = f'TIME: {int(current_time)}'
        cv2.putText(frame, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    def get_minimum_sized_detections(self, detections: sv.Detections) -> sv.Detections:
        w = detections.xyxy[:, 2] - detections.xyxy[:, 0]
        h = detections.xyxy[:, 3] - detections.xyxy[:, 1]
        
        detections = detections[
            (w / self.width > 0.05) & # > 5% width
            (h / self.height > 0.05) # > 5% height
        ]
        
        return detections
    
    def predict(self, frame):
        results = self.model(
            frame, conf=self.confidence
        )[0]
        
        detections = sv.Detections.from_ultralytics(results)
        #detections = self.get_minimum_sized_detections(detections)
        detections = self.tracker.update_with_detections(detections)
       
        labels = [
            f"#{tracker_id} {results.names[class_id]}"
            for class_id, tracker_id
            in zip(detections.class_id, detections.tracker_id)
        ]
       
        annotated_frame = self.annotator.annotate(
            scene=frame, detections=detections
        )
        
        annotated_frame = self.label_annotator.annotate(
            scene=frame, detections=detections, labels=labels
        )
        return annotated_frame
    
    def run(self):
        with sv.VideoSink(target_path=self.target, video_info=self.video_info) as sink:
            cap = cv2.VideoCapture(self.source)
            assert cap.isOpened()
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            
            self.start_time = time.time()
            while True:
                ret, frame = cap.read()
                
                frame = self.predict(frame)
                self.frame_count += 1
                
                self.display_fps(frame)
                #self.display_time(frame)
                                
                sink.write_frame(frame)
                cv2.imshow('Object Detection', frame)
                if cv2.waitKey(5) & 0xFF == 27:
                    break
            cap.release()
            cv2.destroyAllWindows()

def get_arguments():
    parser = argparse.ArgumentParser(
        description="Video Processing with YOLO and ByteTrack"
    )
    parser.add_argument(
        "--weights",
        required=True,
        help="Path to the source weights file",
        type=str,
    )
    parser.add_argument(
        "--source",
        required=True,
        help="Path to the source video file",
        type=str,
    )
    parser.add_argument(
        "--target",
        help="Path to the target video file (output)",
        type=str,
        default="result.mp4"
    )
    parser.add_argument(
        "--confidence",
        default=0.3,
        help="Confidence threshold for the model",
        type=float,
    )
    parser.add_argument(
        "--width",
        default=1280,
        help="Resolution of camera",
        type=int,
    )
    parser.add_argument(
        "--height",
        default=960,
        help="Resolution of camera",
        type=int,
    )
    
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = get_arguments()
    detection = ObjectDetection(
        source=args.source,
        target=args.target,
        weights=args.weights,
        confidence=args.confidence,
        width=args.width,
        height=args.height
    )
    
    detection.run()