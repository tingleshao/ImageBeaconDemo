# this class transforms the image into 64 and 64 and with DCT and,
# later add a segmentation map into consideration\


# we may need to insrtall bluez prior to running the program.
# instruction can be found at https://learn.adafruit.com/bluefruit-le-python-library/installation


import cv2
import numpy as np
import zlib

import scipy.io as sio
import gzip
import math

threshold_list = [10, 20, 30, 40, 50, 60]

class image_encoder():
    def init():
        print("Image encoder initialized!")

    def encode_with_constraint(self, img, constraint):
        # assume image is processed
        img_small = cv2.resize(img, (64,64), interpolation=cv2.INTER_CUBIC)
        img_small = np.uint8(img_small)
        img_small_grey = cv2.cvtColor(img_small, cv2.COLOR_BGR2GRAY)
        imf = np.float32(img_small_grey)/255.0  # float conversion/scale
        dst = cv2.dct(imf)           # the dct
        threshold = threshold_list[constraint]
        dst_compress = self.compress_img_constraint(np.int8(dst*10), threshold)
        dst_compress2 = zlib.compress(self.mat_to_byte_array(dst_compress))
        print("compressed length: " + str(len(dst_compress2)))
        return dst_compress, dst_compress2

    def encode_color_with_constraint(self, img, constraint):
        img_small = cv2.resize(img, (64,64), interpolation=cv2.INTER_CUBIC)
        img_small = np.uint8(img_small)
        # dct the image
        #img_small_grey = cv2.cvtColor(img_small, cv2.COLOR_BGR2GRAY)
        imfr = np.float32(img_small[:,:,0]) / 255.0
        imfg = np.float32(img_small[:,:,1]) / 255.0
        imfb = np.float32(img_small[:,:,2]) / 255.0
    #    imf = np.float32(img_small_grey)/255.0  # float conversion/scale
        dstr = cv2.dct(imfr)           # the dct
        dstg = cv2.dct(imfg)           # the dct
        dstb = cv2.dct(imfb)           # the dct

        threshold = threshold_list[constraint]
        dst_compressr = self.compress_img_constraint(np.int8(dstr*10), threshold)
        dst_compressg = self.compress_img_constraint(np.int8(dstg*10), threshold)
        dst_compressb = self.compress_img_constraint(np.int8(dstb*10), threshold)
        dst_compress2 = zlib.compress(self.mat3_to_byte_array(dst_compressr,dst_compressg, dst_compressb ))
        num_array = ""
        for elem in dst_compress2:
            num_array+=(str(elem)+ " ")
        print(num_array)
        print(dst_compress2)
        print(len(zlib.compress(dst_compress2)))
        print(len(dst_compress2))
        return dst_compressr, dst_compressg, dst_compressb, dst_compress2


    def encode(self, img, processed):
        # downsample the image into 64x64
        if not processed:
            img = img[:, 324:2267]
        img_small = cv2.resize(img, (64,64), interpolation=cv2.INTER_CUBIC)
        # dct the image
        img_small = np.uint8(img_small)
        img_small_grey = cv2.cvtColor(img_small, cv2.COLOR_BGR2GRAY)
        imf = np.float32(img_small_grey)/255.0  # float conversion/scale
        dst = cv2.dct(imf)           # the dct
        dst_compress = self.compress_img(np.int8(dst*10))
        dst_compress2 = zlib.compress(self.mat_to_byte_array(dst_compress))
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
        return dst_compress, dst_compress2

    def encode_color(self, img, processed):
        if not processed:
            img = img[:, 324:2267]

        img_small = cv2.resize(img, (64,64), interpolation=cv2.INTER_CUBIC)
        img_small = np.uint8(img_small)
        # dct the image
        #img_small_grey = cv2.cvtColor(img_small, cv2.COLOR_BGR2GRAY)
        imfr = np.float32(img_small[:,:,0]) / 255.0
        imfg = np.float32(img_small[:,:,1]) / 255.0
        imfb = np.float32(img_small[:,:,2]) / 255.0
    #    imf = np.float32(img_small_grey)/255.0  # float conversion/scale
        dstr = cv2.dct(imfr)           # the dct
        dstg = cv2.dct(imfg)           # the dct
        dstb = cv2.dct(imfb)           # the dct

        dst_compressr = self.compress_img(np.int8(dstr*10))
        dst_compressg = self.compress_img(np.int8(dstg*10))
        dst_compressb = self.compress_img(np.int8(dstb*10))
        dst_compress2 = zlib.compress(self.mat3_to_byte_array(dst_compressr,dst_compressg, dst_compressb ))
        num_array = ""
        for elem in dst_compress2:
            num_array+=(str(elem)+ " ")
        print(num_array)
        print(dst_compress2)
        print(len(zlib.compress(dst_compress2)))
        print(len(dst_compress2))
        return dst_compressr, dst_compressg, dst_compressb, dst_compress2

    def mat_to_byte_array(self, mat):
        arr = np.asarray(mat.reshape(1,4096))
        return arr

    def mat3_to_byte_array(self, mat0, mat1, mat2):
        mat3 = np.array([mat0, mat1, mat2])
        arr = np.asarray(mat3.reshape(1,4096*3))
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
            #    if i + j > 30:
                if i + j > 60:
                    dst_new[i,j] = 0
                else:
                    count = count+1
        print("dst new:")
        print(dst_new)
        return dst_new

    def compress_img_constraint(self, dst, constraint):
        dst_new = dst.copy()
        count = 0
        for i in range(dst.shape[0]):
            for j in range(dst.shape[1]):
                if i + j > constrant:
                    dst_new[i, j] = 0
                else:
                    count = count + 1
        return dst_new

    def prepare(self, data):
        # prepare the data to be broadcasted
        num_array = []
        for elem in data:
            num_array.append(int(elem))
        result_array = []
        for i in range(math.ceil(len(num_array) / 20)):
            curr_array = []
            curr_array.append(i+1)
            curr_array = curr_array + num_array[i*20:((i+1)*20+1)]
            result_array.append(curr_array)
        return result_array

    def decode(self, dst):
        img = cv2.idct(np.float32(dst)/10.0)
        return img
