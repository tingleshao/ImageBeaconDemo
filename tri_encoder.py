# encode input image using triangularization

import cv2
import numpy as np

# ? 
class tri_encoder():
    def init():
        print("Triangle encoer initialized!")

    def encode(self, img, processed):
        # downsample image into 64 x 64
        if not processed:
            img = img[:, 324:2267]
        img_small = cv2.resize(img, (64, 64), interpolation=cv2.INTER_CUBIC)
        # triangularization the image
