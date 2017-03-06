# always seem to need this
import sys
import cv2
# This gets the Qt stuff
import PyQt5
from PyQt5.QtWidgets import *

from image_segmenter import image_segmenter
import argparse as ap
# This is our window from QtCreator
import mainwindow_auto
from image_encoder import image_encoder
from data_broadcaster import data_broadcaster
import time, threading
import picamera



# create class for our Raspberry Pi GUI
class MainWindow(QMainWindow, mainwindow_auto.Ui_MainWindow):
    # access variables inside of the UI's file
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self) # gets defined in the UI file
        self.pushButton.clicked.connect(self.buttonClicked)
        self.pushButton2.clicked.connect(self.button2Clicked)
        self.broadcaster = data_broadcaster()
        self.index = 0
        self.packets = []
        self.camera = picamera.PiCamera()


    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' was pressed')
        image = cv2.imread("image.jpg")
        encoder = image_encoder()
        img_data, encoded_img_data = encoder.encode(image)
        cv2.imshow("output", encoder.decode(img_data))
        print(encoded_img_data)
        self.set_data(encoded_img_data)

        print("self data:" + str(self.data))
        encoder = image_encoder()
        self.packets = encoder.prepare(self.data)

        self.broadcast_image()
        print("button clicked!")

    def button2Clicked(self):
        self.camera.start_preview(fullscreen=False, window=(10,20,640,480))
        signal = input()
        self.camera.stop_preview()
        self.camera.capture("image.jpg")

    def set_data(self, data):
        self.data = data

    def broadcast_image(self):
        print("packets"+ str(self.packets))
        print("index"+str(self.index))
        self.broadcaster.broadcast_data(self.packets[self.index])
        self.index = self.index +1
        if self.index >= len(self.packets):
            self.index = 0
        threading.Timer( 1, self.broadcast_image ).start()

# I feel better having one of these
def main():
    # read input image path
#    ap.add_argument("-i", "--image", required=True, help="path to input image")
#    args = vars(apl.parse_args())
#    image = cv2.imread(args["image"])
#    image = cv2.imread("Lenna.png")
 #   shifted = cv2.pyrMeanShiftFiltering(image, 21, 51)
#    cv2.imshow("Input", image)

#    encoder = image_encoder()
#    img_data, encoded_img_data = encoder.encode(image)
#    cv2.imshow("output", encoder.decode(img_data))
#    print(encoded_img_data)
#    print(len(encoded_img_data))
#    segmenter = image_segmenter()
#    segmenter.watershed(shifted)
    # a new app instance
    app = QApplication(sys.argv)
    form = MainWindow()
#    form.set_data(encoded_img_data)
    form.horizontalSlider_3.setProperty("value", 0)
    form.show()
    # without this, the script exits immediately.
    sys.exit(app.exec_())


# python bit to figure how who started This
if __name__ == "__main__":
 main()
