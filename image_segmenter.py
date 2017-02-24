
#TODO: implement watershed first.

from skimage.feature import peak_local_max
from skimage.morphology import watershed
from scipy import ndimage
import argparse
import cv2

from matplotlib import pyplot as plt

class image_segmenter():
    def set_images(image1, image2):
        self.image1 = image1
        self.image2 = image2

    def segment():
        return None

    def watershed(image):
        gray = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)
        # Otsu
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        cv2.imshow("Thresh", thresh)
        # Watershed
        # find contours in the thresholded image
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        print("[INFO] {} unique contours found".format(len(cnts)))
        # loop over the contours
        for (i, c) in enumerate(cnts):
            # draw the contour
            ((x, y), _) = cv2.minEnclosingCircle(c)
            cv2.putText(image, "#{}".format(i+1), (int(x) - 10, int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        # show the output image
        cv2.imshow("Image", image)
        cv2.waitKey(0)
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

    def disparity(image1, image2):
        stereo = cv2.createStereoBM(numDisparities=16, blockSize=15)
        disparity = stereo.compute(image1, image2)
        plt.imshow(disparity, 'gray')
        plt.show()

    
