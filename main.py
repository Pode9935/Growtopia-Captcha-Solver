from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
from flask import Flask
from ultralytics import YOLO
import urllib3
import os

app = Flask(__name__)

model = YOLO('best.pt')

@app.route('/captcha=<string:pid>')
def captcha(pid):
    rttex_path = r'data\{}.rttex'.format(pid)
    img_path = r'data\{}.png'.format(pid)
    failed_path = r'failed\{}.png'.format(pid)
    solved_path = r'solved\{}.png'.format(pid)

    if not os.path.exists(rttex_path):
        url = 'https://ubistatic-a.akamaihd.net/0098/captcha/generated/{}-PuzzleWithMissingPiece.rttex'.format(pid)
        http = urllib3.PoolManager()
        r = http.request('GET', url)
        if r.status == 200:
            with open(r'data\{}.rttex'.format(pid), 'wb') as f:
                f.write(r.data)

        else:
            return 'Failed'

    if not os.path.exists(img_path) and os.path.exists(rttex_path):
        with open(r'data\{}.rttex'.format(pid), 'rb') as image:
            data = image.read()

        width = int.from_bytes(data[12:16], byteorder='little')
        height = int.from_bytes(data[8:12], byteorder='little')

        imgs = Image.frombytes(mode='RGBA', size=(width, height), data=data[0x7c:])
        imgs = imgs.transpose(method=Image.FLIP_TOP_BOTTOM)

        imgs.save(r'data\{}.png'.format(pid), format='PNG')

    if os.path.exists(img_path):
        ans = ''
        img = Image.open(r'data\{}.png'.format(pid))
        reresults = model.predict(img, conf=0.6)
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
                if not os.path.exists(failed_path):
                    img.save(r'failed\{}.png'.format(pid), 'PNG')

                ans = 'Failed'

        if ans != 'Failed':
            if not os.path.exists(solved_path):
                img.save(r'solved\{}.png'.format(pid), 'PNG')

        return ans

@app.route('/')
def index():
    return "Growtopia captcha solver"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="80")
