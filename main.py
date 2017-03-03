# always seem to need this
import sys

# This gets the Qt stuff
import PyQt5
from PyQt5.QtWidgets import *

from image_segmenter import image_segmenter
import argparse
# This is our window from QtCreator
import mainwindow_auto



# create class for our Raspberry Pi GUI
class MainWindow(QMainWindow, mainwindow_auto.Ui_MainWindow):
    # access variables inside of the UI's file
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self) # gets defined in the UI file

# I feel better having one of these
def main():

    # read input image path
#    ap.add_argument("-i", "--image", required=True, help="path to input image")
#    args = vars(apl.parse_args())

#    image = cv2.imread(args["image"])
 #   shifted = cv2.pyrMeanShiftFiltering(image, 21, 51)
 #   cv2.imshow("Input", image)

#    segmenter = image_segmenter()
#    segmenter.watershed(shifted)
    # a new app instance
    app = QApplication(sys.argv)
    form = MainWindow()
    form.horizontalSlider_3.setProperty("value", 0)

    form.show()
    # without this, the script exits immediately.
    sys.exit(app.exec_())


# python bit to figure how who started This
if __name__ == "__main__":
 main()
