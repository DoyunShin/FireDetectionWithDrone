class dummy():
    def __init__(self):
        pass


class dji():
    def __init__(self, storage):
        import importlib
        from djitellopy import tello

        self.storage = storage
        self.modules = dummy()
        self.modules.time = importlib.import_module('time')
        self.modules.base64 = importlib.import_module('base64')
        
        self.drone = tello.Tello()


        self.battery = 0
        self.detected = False
        self.detectedtime = 0
        self.image = None
        self.image_base64 = None
        self.lat = 37.401946
        self.lng = 126.664773

        self.connect()
        pass

    def connect(self):
        self.drone.connect()
        self.drone.streamon()
        pass

    def frame(self):
        return self.drone.get_frame_read().frame

    def close(self):
        self.drone.close()
        pass

    def autoupdate(self):
        self.battime = self.modules.time.time()
        self.battery = self.drone.get_battery()
        while True:
            print("DETECT", self.detected)
            if self.modules.time.time() - self.storage.summarytime < 20:
                if self.modules.time.time() - self.battime > 30:
                    self.battime = self.modules.time.time()
                    self.battery = self.drone.get_battery()
                
                detected_image, output_objects_array, detected_objects_image_array = self.storage.firenet.detect(self.drone.get_frame_read().frame)
                # deted_image to base64
                detected_image = self.storage.firenet.modules.cv2.imencode('.png', detected_image)[1].tobytes()
                self.image_base64 = self.modules.base64.b64encode(detected_image).decode('utf-8')
                self.image = detected_image
                if output_objects_array != []:
                    self.detected = True
                    self.detectedtime = self.modules.time.time()
                else:
                    # if self.detectedtime is after 10 sec
                    if self.modules.time.time() - self.detectedtime > 60:
                        self.detected = False
                        self.detectedtime = 0
                #self.modules.time.sleep(1)
                pass
        pass

#    def send(self):
#        self.drone.send_command_with_return("")

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
