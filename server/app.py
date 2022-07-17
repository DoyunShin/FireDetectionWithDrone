class dummy():
    def __init__(self):
        pass

class Storage():
    def __init__(self):
        from dji import dji
        from firenet import firenet

        self.dji = dji(self)
        self.firenet = firenet(self)


        pass

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

@app.route('/api/dji/status/<string>', methods=['GET'])
def dji_status(string):
    return storage.dji.status_drone()

@app.route('/api/dji/frame/<string>', methods=['GET'])
def dji_frame(string):
    return storage.dji.frame()

@app.route('/api/dji/frame-detect/<string>', methods=['GET'])
def dji_frame_detect(string):
    image, output_objects_array, detected_objects_image_array = storage.firenet.detect(storage.dji.frame())
    return storage.firenet.modules.cv2.imencode('.jpg', image)[1].tobytes(), 200


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080, debug=True)


