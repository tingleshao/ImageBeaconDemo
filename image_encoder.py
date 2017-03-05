# this class basically, transforms the image into 64 and 64 and with DCT and,
# later add a segmentation map into consideration\


# we may need to insrtall bluez prior to running the program.
# instruction can be found at https://learn.adafruit.com/bluefruit-le-python-library/installation


import cv2
import numpy as np
import zlib

import scipy.io as sio
import gzip

class image_encoder():
    def init():
        print("Image encoder initialized!")

    def encode(self, img):
        # downsample the image into 64x64
        img_small = cv2.resize(img, (64,64), interpolation=cv2.INTER_CUBIC)
        # dct the image
        img_small_grey = cv2.cvtColor(img_small, cv2.COLOR_BGR2GRAY)
        imf = np.float32(img_small_grey)/255.0  # float conversion/scale
        dst = cv2.dct(imf)           # the dct
        # TODO: add statistical compression on it.
    #    return dst
        dst_compress = self.compress_img(np.int8(dst*10))
        dst_compress2 = zlib.compress(self.mat_to_byte_array(dst_compress))
##

    #    dst_array = [elem.encode("hex") for elem in dst_compress2]
        num_array = ""
        for elem in dst_compress2:
            num_array+=(str(elem)+ " ")
        print(num_array)
    #    print(dst_array)
    #    print(len(dst_array))
        print(dst_compress2)
        print(len(zlib.compress(dst_compress2)))
        print(len(dst_compress2))
    #    f_out = gzip.open("compress", 'wb')
    #    sio.savemat(f_out, do_compression = True)

        return dst_compress
    #    imgcv1 = np.uint8(dst)*255.0    # convert back

    def mat_to_byte_array(self, mat):
        arr = np.asarray(mat.reshape(1,4096))
        return arr

    def quantize_dct(self, dst):
        dst_copy = dst
        return None

    def encode_image_with_segmentation(img, mask):
        return None

    def encode_image_mesh(img, mask):
        # we may find a better mesh method using this link:
        # https://people.eecs.berkeley.edu/~jrs/?_ga=1.243688709.1020511277.1487973402
        # there is another related repository on GitHub.
        return None

    def compress_img(self, dst):
        dst_new = dst.copy()
        count = 0
        for i in range(dst.shape[0]):
            for j in range(dst.shape[1]):
                if i + j > 30:
                    dst_new[i,j] = 0
                else:
                    count = count+1
        print("dst new:")
        print(dst_new)
        return dst_new

    def prepare(self, data):
        # prepare the data to be broadcasted
        

    def decode(self, dst):
        img = cv2.idct(np.float32(dst)/10.0)
        return img
