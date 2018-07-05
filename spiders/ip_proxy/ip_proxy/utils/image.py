# coding = utf-8

from PIL import Image
import pytesseract
from io import BytesIO
import random

class Img(object):

    def __init__(self, cmd = None):
        self.pytsract = pytesseract
        if cmd:
            self.pytsract.pytesseract.tesseract_cmd = cmd
        pass

    def parse(self, content):
        image = self.rmline(BytesIO(content))
        text = self.pytsract.image_to_string(image)
        return text
        # image = Image.open(BytesIO(content))
        # img = image.convert('L')
        # bimg = self.binarizing(img, 190)
        # dimg = self.depoint(bimg)
        # text = self.pytsract.image_to_string(dimg)
        # return text

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

    # 去除干扰线
    def rmline(self, content):
        image = Image.open(content)
        image_array = image.load()
        x,y = image.size
        for i in range(x):
            for j in range(y):
                if image_array[i, j] != (0, 0, 0, 255):
                    image_array[i, j] = (0, 0, 0, 0)
        return image

    # 边界检测
    def check_col(image_array_a, col, y_num):
        this_col = False
        for jj in range(y_num):
            if image_array_a[col, jj] != (0, 0, 0, 0):
                this_col = True
        return this_col

    # 字符位置检测
    def position(self, image_array):
        crop_position_array = []
        start_flag = False
        start_ci = 0
        for ci in range(x):
            check_col_result = check_col(image_array, ci, y)
            print(check_col_result, ci)
            if start_flag and not check_col_result:
                crop_item = (start_ci, 0, ci, 9)
                crop_position_array.append(crop_item)
                start_flag = False
                start_ci = 0
            if not start_flag and check_col_result:
                start_flag = True
                start_ci = ci
        # 切割所有字符
        index = 0
        for cro_i in crop_position_array:
            print(cro_i)
            image.crop(cro_i).save('./code/' + str(index) + '.png')
            index += 1

img = Img()


    