# this class basically, transforms the image into 64 and 64 and with DCT and,
# later add a segmentation map into consideration\


# we may need to insrtall bluez prior to running the program.
# instruction can be found at https://learn.adafruit.com/bluefruit-le-python-library/installation


import cv2
import numpy as np

class image_encoder():
    def init():
        print("Image encoder initialized!")

    def encode(self, img):
        # downsample the image into 64x64
        img_small = cv2.resize(img, (64,64), interpolation=cv2.INTER_CUBIC)
        # dct the image
        imf = np.float32(img_small)/255.0  # float conversion/scale
    #    dst = cv2.dct(imf)           # the dct
        # TODO: add statistical compression on it.
    #    return dst
        return None
    #    imgcv1 = np.uint8(dst)*255.0    # convert back

    def encode_image_with_segmentation(img, mask):
        return None

    def encode_image_mesh(img, mask):
        # we may find a better mesh method using this link:
        # https://people.eecs.berkeley.edu/~jrs/?_ga=1.243688709.1020511277.1487973402
        # there is another related repository on GitHub.
        return None
