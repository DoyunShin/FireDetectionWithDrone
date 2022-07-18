class dummy():
    def __init__(self):
        pass


class firenet():
    def __init__(self, storage):
        self.storage = storage

        import importlib

        


        self.modules = dummy()
        self.modules.cv2 = importlib.import_module('cv2')
        self.modules.time = importlib.import_module('time')
        self.modules.PIL = importlib.import_module('PIL')
        self.modules.six = importlib.import_module('six')

        self.load_model()
        pass

    def load_model(self):
        from imageai.Detection.Custom import CustomObjectDetection
        self.detector = CustomObjectDetection()
        self.detector.setModelTypeAsYOLOv3()
        self.detector.setModelPath("detection_model-ex-33--loss-4.97.h5")
        self.detector.setJsonPath("detection_config.json")
        self.detector.loadModel()
        pass

    def detect(self, frame):
        drawn_image, output_objects_array, detected_objects_image_array = self.detector.detectObjectsFromImage(input_type="array", input_image=frame, output_type="array", extract_detected_objects=True)
        return drawn_image, output_objects_array, detected_objects_image_array
        pass

#https://github.com/OlafenwaMoses/FireNET/releases/download/v1.0/detection_model-ex-33--loss-4.97.h5