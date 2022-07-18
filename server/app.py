class dummy():
    def __init__(self):
        pass

class Storage():
    def __init__(self):
        from dji import dji
        from firenet import firenet
        from threading import Thread
        import time

        self.dji = dji(self)
        self.firenet = firenet(self)
        self.Thread = Thread
        self.time = time

        self.summarytime = 0

        self.autosetup()


        pass
    
    def autosetup(self):
        self.autoupdate = self.Thread(target=self.dji.autoupdate)
        self.autoupdate.start()


from flask import *
from flask_compress import Compress
from flask_cors import CORS
import os

storage = Storage()
compress = Compress()
app = Flask(__name__)
app.secret_key = os.urandom(12)
CORS(app)

@app.route('/')
def nf():
    return {"status": 404, "message": "Not Found"}, 404

@app.route('/api/')
def nf2():
    return {"status": 404, "message": "Not Found"}, 404

@app.route('/api/drone/locateinfo', methods=['GET'])
def dji_status():
    rtn = {"status": 200, "message": "OK"}
    data = {}
    data.update({"lat": storage.dji.lat})
    data.update({"lng": storage.dji.lng})
    rtn.update({"data": data})
    return rtn, 200

@app.route('/api/drone/locateinfo_summary', methods=['GET'])
def dji_frame():
    if storage.time.time() - storage.summarytime > 20:
        storage.summarytime = storage.time.time()
        storage.time.sleep(2)
    else:
        storage.summarytime = storage.time.time()

    rtn = {"status": 200, "message": "OK"}
    data = {}
    data.update({"detected": storage.dji.detected})
    #print("DET OK")
    data.update({"battery": str(storage.dji.battery)})
    #print("BAT OK")
    data.update({"image": storage.dji.image_base64})
    #print("IMG OK")
    data.update({"lat": storage.dji.lat})
    #print("LAT OK")
    data.update({"lng": storage.dji.lng})
    #print("LNG OK")
    rtn.update({"data": data})
    return rtn, 200

@app.route('/api/drone/image')
def dji_image():
    if storage.time.time() - storage.summarytime > 20:
        storage.summarytime = storage.time.time()
        storage.time.sleep(2)
    else:
        storage.summarytime = storage.time.time()
    return storage.dji.image, 200

@app.route('/api/drone/connect')
def dji_connect():
    storage.dji.connect()
    return {"status": 200, "message": "OK"}, 200
#@app.route('/api/dji/frame-detect/<string>', methods=['GET'])
#def dji_frame_detect(string):
#    image, output_objects_array, detected_objects_image_array = storage.firenet.detect(storage.dji.frame())
#    return storage.firenet.modules.cv2.imencode('.jpg', image)[1].tobytes(), 200


if __name__ == '__main__':
    app.debug = True
    #import logging
    #storage.dji.drone.LOGGER.setLevel(logging.DEBUG)

    
    app.run(host='127.0.0.1', port=8080, debug=True, use_reloader=False)


