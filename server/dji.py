from server.app import storage


class dummy():
    def __init__(self):
        pass


class dji():
    def __init__(self, storage):
        import importlib

        self.storage = storage
        self.modules = dummy()
        self.modules.dji = importlib.import_module('dji').tello
        self.modules.time = importlib.import_module('time')
        
        
        self.drone = self.modules.dji.Tello()
        pass

    def connect(self):
        self.drone.connect()
        self.drone.streamon()
        pass

    def status_drone(self):
        return self.drone.get_battery()
        pass

    def frame(self):
        return self.drone.get_frame_read().frame

    def close(self):
        self.drone.close()
        pass


if __name__=="__main__":
    from firenet import firenet
    storage = dummy()
    dji = dji(storage)
    firenet = firenet(storage)

    dji.connect()
    print("BATTERY", dji.status_drone())

    while True:
        frame = dji.frame()
        drawn_image, output_objects_array, detected_objects_image_array = firenet.detect(dji.frame())
        firenet.modules.cv2.imshow("Frame", drawn_image)
        print("output_objects_array", output_objects_array)
        print("detected_objects_image_array", detected_objects_image_array)
        print("==========================================================")
        if firenet.modules.cv2.waitKey(1) & 0xFF == ord('q'): break
        pass
