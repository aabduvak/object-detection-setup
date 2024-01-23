from PyQt5 import QtWidgets as qt
from PyQt5 import uic
from PyQt5.QtCore import QLibraryInfo
from datetime import datetime
from stream import ObjectDetection
import uuid



class Window(qt.QMainWindow):
    def __init__(self):
        super().__init__()

        #this is used for loading ui file
        uic.loadUi("assets/main.ui", self)
                
        self.main_layout = self.findChild(qt.QVBoxLayout, 'mainLayout')
            
        self.confidence = None
        self.source = None
        self.model = None
        
        # choose model
        self.model_btn = self.findChild(qt.QPushButton, "modelButton")
        self.model_btn.clicked.connect(self.chooseModel)
        
        # choose confidence
        self.confidence_slider = self.findChild(qt.QSlider, "confidenceSlider")
        self.confidence_slider.valueChanged.connect(self.setConfidence)
        
        # choose source type
        self.source_box = self.findChild(qt.QComboBox, "sourceBox")
        self.source_box.currentIndexChanged.connect(self.setSourceType)
    
        # choose source
        self.source_btn = self.findChild(qt.QPushButton, "sourceButton")
        self.source_btn.clicked.connect(self.setSource)
        
        # start action
        self.start_btn = self.findChild(qt.QPushButton, "startButton")
        self.start_btn.clicked.connect(self.start)
    
    def start(self):
        if self.source == None or self.source == '':
            qt.QMessageBox.warning(self, "Invalid source", "Source must be specified")
            return
        
        if not self.confidence:
            qt.QMessageBox.warning(self, "Invalid confidence", "Confidence must be specified")
            return
        
        if not self.model:
            qt.QMessageBox.warning(self, "Invalid model", "Model must be specified")
            return
        
        target = f'results/{datetime.now().strftime("%d-%m-%Y_%H:%M:%S")}-{uuid.uuid4()}.mp4'
        conf = float(self.confidence / 100)
        
        detection = ObjectDetection(self.source, target, conf, self.model, 1280, 960)
        detection.run()
    
    def setSource(self):
        options = qt.QFileDialog.Options()
        
        self.source, _ = qt.QFileDialog.getOpenFileName(self, "Open File", "", "Video (*.mp4);;All Files (*)", options=options)
        if self.source:
            filename = self.source.split("/")[-1]
            if len(filename) > 10:
                filename = filename.split(".")[0][:10] + "...mp4"
            self.source_btn.setText(f'Selected File: {filename}')
    
    def setSourceType(self, index):
        if index == 0:
            qt.QMessageBox.information(self, "Invalid input", "Please select valid source type")
            return
        
        self.source_type = self.source_box.currentText()
        if index == 1: # webcam
            self.source = '0'
        
        elif index == 2:
            self.source = ''
    
        
    def setConfidence(self):
        self.confidence = self.confidence_slider.value()
        self.confidence_label = self.findChild(qt.QLabel, "cofidenceValue")
        self.confidence_label.setText(f'{self.confidence}%')
    
    def chooseModel(self):
        options = qt.QFileDialog.Options()
        
        self.model, _ = qt.QFileDialog.getOpenFileName(self, "Open File", "", "Models (*.pt);;All Files (*)", options=options)
        if self.model:
            self.model_btn.setText(f'Selected File: {self.model.split("/")[-1]}')
