from PIL import Image
from io import BytesIO
from flask import Flask
from ultralytics import YOLO
import shutil
import urllib3

app = Flask(__name__)

model = YOLO('best.pt')

def RTTEX_PNG(name):
    with open('data/{}.rttex'.format(name), 'rb') as image:
        data = image.read()

    width = int.from_bytes(data[12:16], byteorder='little')
    height = int.from_bytes(data[8:12], byteorder='little')

    img = Image.frombytes(mode='RGBA', size=(width, height), data=data[0x7c:])
    img = img.transpose(method=Image.FLIP_TOP_BOTTOM)

    buffer = BytesIO()
    img.save(buffer, format='PNG')
    png_data = buffer.getvalue()

    with open('data/{}.png'.format(name), 'wb') as simg:
        simg.write(png_data)

def yolov8(name):
    reresults = model('data/{}.png'.format(name), conf=0.5)
    for result in reresults:
        boxes = result.boxes
        if not 'tensor([],' in str(boxes.xyxy):
            for bbox in boxes:
                for i, box in enumerate(bbox.xyxy):
                    x, y, w, h = [int(i) for i in box]
                    return str(x / 512)

        else:
            shutil.copyfile('data/{}.png'.format(name), 'failed/{}.png'.format(name))
            return 'Failed'

@app.route('/captcha=<string:pid>')
def captcha(pid):
    url = 'https://ubistatic-a.akamaihd.net/0098/captcha/generated/{}-PuzzleWithMissingPiece.rttex'.format(pid)
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    if r.status == 200:
        with open('data/{}.rttex'.format(pid), 'wb') as f:
            f.write(r.data)

        RTTEX_PNG(pid)
        return yolov8(pid)

    else:
        return 'Failed'

@app.route('/')
def index():
    return "Growtopia captcha solver"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="80", threaded=True)
