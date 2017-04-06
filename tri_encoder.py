# encode input image using triangularization

import cv2
import numpy as np
import drawTriangles as dt

#
class tri_encoder():
    def init():
        print("Triangle encoer initialized!")

    def encode(self, img, processed, filename):
        # downsample image into 64 x 64
        if not processed:
            img = img[:, 324:2267]
        img_small = cv2.resize(img, (64, 64), interpolation=cv2.INTER_CUBIC)
        # triangularization the image
        (color_im, black_im) = dt.loadAndFilterImage(filename)
        (width, height) = color_im.size
        multiplier = 10

        points = dt.findPointsFromImage(black_im)
        triangles = dt.delaunayFromPoints(points)
        polygons = voronoiFromTriangles(triangles)

        dt.drawImageColoredTriangles(triangles, "delaunay_" + filename, color_im, multiplier)
        dt.drawImageColoredTriangles(polygons, "voronoi_" + filename, color_im, multiplier)

        # TODO: is this a postprocessing stage? shall I add it into the client?
        dt.autocontrastImage("voronoi_" + filename)
        dt.autocontrastImage("delaunay_" + filename)

        b = cv2.imread("delaunay_" + filename)
        return b
