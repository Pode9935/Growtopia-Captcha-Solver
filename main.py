from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
from flask import Flask
from ultralytics import YOLO
import urllib3

app = Flask(__name__)

model = YOLO('best.pt')

def RTTEX_PNG(name):
    with open(r'data\{}.rttex'.format(name), 'rb') as image:
        data = image.read()

    width = int.from_bytes(data[12:16], byteorder='little')
    height = int.from_bytes(data[8:12], byteorder='little')

    imgs = Image.frombytes(mode='RGBA', size=(width, height), data=data[0x7c:])
    imgs = imgs.transpose(method=Image.FLIP_TOP_BOTTOM)

    imgs.save(r'data\{}.png'.format(name), format='PNG')

def yolov8(name):
    ans = ''
    img = Image.open(r'data\{}.png'.format(name))
    reresults = model.predict(img, conf=0.8)
    for result in reresults:
        boxes = result.boxes
        if not 'tensor([],' in str(boxes.xyxy):
            for bbox in boxes:
                for i, box in enumerate(bbox.xyxy):
                    x, y, w, h = [int(i) for i in box]
                    font = ImageFont.truetype(r'ayar.ttf', 15)
                    text = "Puzzle: {}".format(round(float(bbox.conf), 6))
                    img1 = ImageDraw.Draw(img)
                    img1.rectangle([x, y, w, h], outline = "#ff00ff", width = 2)
                    img1.rectangle([x, y - 20, x + font.getlength(text), y], fill = "#ff00ff", outline = "#ff00ff")
                    img1.text((x, y - 20), text, fill = "black", font = font)
                    ans = str(x / 512)

        else:
            img.save(r'failed\{}.png'.format(name), 'PNG')
            ans = 'Failed'

    if ans != 'Failed':
        img.save(r'solved\{}.png'.format(name), 'PNG')

    return ans

@app.route('/captcha=<string:pid>')
def captcha(pid):
    url = 'https://ubistatic-a.akamaihd.net/0098/captcha/generated/{}-PuzzleWithMissingPiece.rttex'.format(pid)
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    if r.status == 200:
        with open(r'data\{}.rttex'.format(pid), 'wb') as f:
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
