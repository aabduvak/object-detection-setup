# YOLOv8 Object Detection Setup 🤖 📷

This repository facilitates the implementation of object detection using the YOLOv8 algorithm. Users can effortlessly run their models, and the program will automatically generate output videos in the **results** folder. Sample models are included for quick and easy usage.

## Overview

The `YOLOv8` Object Detection Setup allows users to perform real-time object detection using the YOLOv8 algorithm. The project is designed for simplicity and convenience, enabling users to run their models seamlessly and obtain output videos with detected objects.

## Prerequisites
Ensure the following dependencies are installed:
- Python 3.x
- YOLOv8 (refer to YOLOv8 documentation for installation instructions)
- Nvidia CUDA Framework (optional)

## Installation (windows)
1. Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/aabduvak/object-detection-setup.git setup ;
cd setup
```
2. Install required packages
```bash
pip install -r requirements.txt
```
If there is conflict on version of packages
```bash
pip install ultralytics supervision PyQt5 opencv-contrib-python
```
## Usage
Run model with GUI (PyQt5), choose model and source
```bash
python main.py
```

<img src="https://github.com/aabduvak/object-detection-setup/blob/main/assets/example.gif">

Run model in command-line
```bash
python stream.py --source=path-to-source --weights=path-to-model --target=output.mp4
```
Example
```bash
python stream.py --weights=models/person.pt --target=result.mp4 --source=0 #webcam
```

## Customization

You can easily customize the object detection system by modifying configurations, integrating your own YOLOv8 models, or adjusting other parameters as needed.<br> <br>
For more info: <br>
https://docs.ultralytics.com/modes/train/#introduction

## Contributing
Contributions are welcome! 🙃

## Contact

For support, feedback, or questions, please contact abdulaziz.yosk@gmail.com or open an issue on the GitHub repository.
