

from skimage.feature import peak_local_max
from skimage.morphology import watershed
from scipy import ndimage
import argparse
import cv2
import numpy as np

from matplotlib import pyplot as plt

class image_segmenter():
    def set_images(image1, image2):
        self.image1 = image1
        self.image2 = image2

    def segment():
        return None

    def watershed(self,image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Otsu
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
#        cv2.imshow("Thresh", thresh)
        # Watershed
        # find contours in the thresholded image
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        print("[INFO] {} unique contours found".format(len(cnts)))
        # loop over the contours
  #      for (i, c) in enumerate(cnts):
   #         # draw the contour
    #        ((x, y), _) = cv2.minEnclosingCircle(c)
     #       cv2.putText(image, "#{}".format(i+1), (int(x) - 10, int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
      #      cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        # show the output image
    #    cv2.imshow("Image", image)
    #    cv2.waitKey(0)
        # wait, the code above are just another example that does not work

        # watershed beings from here
        D = ndimage.distance_transform_edt(thresh)
        localMax = peak_local_max(D, indices=False, min_distance=20, labels=thresh)
        # perform a connected component analysis on the local peaks,
        # using 8-connectivity, then apply the watershed algorithm
        markers = ndimage.label(localMax, structure=np.ones((3,3)))[0]
        labels = watershed(-D, markers, mask=thresh)
        print("[INFO] {} unique segments found".format(len(np.unique(labels))-1))
        # loop over the unique labels returned by the watershed algorithm
        for label in np.unique(labels):
            # if the label is zero, we are examing the background, so simply ignore it
            if label == 0:
                continue
            # otherwise allocate memory for the label region and draw it on the mask
            mask = np.zeros(gray.shape, dtype="uint8")
            mask[labels == label] = 255
            # detect contours in the mask and grab the largest one
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            c = max(cnts, key=cv2.contourArea)
            # draw a circle enclosing the object
            ((x, y), r) = cv2.minEnclosingCircle(c)
            cv2.circle(image, (int(x), int(y)), int(r), (0, 255, 0), 2)
            cv2.putText(image, "#{}".format(label), (int(x)-10, int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        # show the output image
        cv2.imshow("Output", image)
        cv2.waitKey(0)

    def disparity(self, image1, image2):
        image1copy = image1
        image1=cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        image2=cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        stereo = cv2.StereoBM_create( numDisparities=16, blockSize=15)
        disparity = stereo.compute(image1, image2)
        print("disparity" + str(disparity))
        binary_disparity = self.convertToBinary(disparity, 200, 200)
        ref_bin = self.refine(binary_disparity)
        res = self.processImage(image1copy, ref_bin) 
#        plt.imshow(res)
        return res        
 #       plt.show()

    def convertToBinary(self, dis, w, h):
        bin = np.zeros([h,w])
        for i in range(w):
            for j in range(h):
                if dis[j,i] > -16:
                    bin[j,i] = 1 
        return bin

    def refine(self, bin):
        kernel1 = np.ones((3,3), np.uint8)
        kernel2 = np.ones((20,20), np.uint8)
         
        ref1 = cv2.erode(bin, kernel1, iterations=1)
        ref2 = cv2.dilate(ref1, kernel2, iterations=1)
        return ref2
 
    def processImage(self, img, bin): 
        # img: 64, 64
        img = cv2.resize(img, (64,64), interpolation=cv2.INTER_CUBIC)
        bin = cv2.resize(bin, (64,64), interpolation=cv2.INTER_CUBIC)
        fg = np.zeros((64,64,3))
        bg = np.zeros((64,64,3)) 
        for i in range(64): 
            for j in range(64):
                if bin[j,i] > 0:
                    fg[j,i] = img[j,i]
                else: 
                    bg[j,i] = img[j,i]
        bg = cv2.resize(bg, (5,5), interpolation=cv2.INTER_CUBIC)
        bg = cv2.resize(bg, (64,64), interpolation=cv2.INTER_CUBIC)
        res = np.zeros((64,64,3))
  #      plt.imshow(bg)
   #     plt.imshow(fg)
        cv2.imwrite('fg.jpg', fg)
        cv2.imwrite('bg.jpg', bg)
        for i in range(64):
            for j in range(64):
                res[j,i,:] = fg[j,i,:] + bg[j,i,:]
        cv2.imwrite('res.jpg', res)
        return res
