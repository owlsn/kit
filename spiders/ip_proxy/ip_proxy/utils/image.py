# coding = utf-8

from PIL import Image
import pytesseract
from io import BytesIO

class Img(object):

    def __init__(self, cmd = None):
        self.pytsract = pytesseract
        if cmd:
            self.pytsract.pytesseract.tesseract_cmd = cmd
        pass

    def parse(self, content):
        image = Image.open(BytesIO(content))
        img = image.convert('L')
        bimg = self.binarizing(img, 190)
        dimg = self.depoint(bimg)
        text = self.pytsract.image_to_string(dimg)
        return text

    # 二值化算法
    def binarizing(self, img,threshold):
        pixdata = img.load()
        w, h = img.size
        for y in range(h):
            for x in range(w):
                if pixdata[x, y] < threshold:
                    pixdata[x, y] = 0
                else:
                    pixdata[x, y] = 255
        return img

    # 去除干扰线算法
    def depoint(self, img):   #input: gray image
        pixdata = img.load()
        w,h = img.size
        for y in range(1,h-1):
            for x in range(1,w-1):
                count = 0
                if pixdata[x,y-1] > 245:
                    count = count + 1
                if pixdata[x,y+1] > 245:
                    count = count + 1
                if pixdata[x-1,y] > 245:
                    count = count + 1
                if pixdata[x+1,y] > 245:
                    count = count + 1
                if count > 2:
                    pixdata[x,y] = 255
        return img


    