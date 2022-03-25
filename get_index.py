import dlib
import cv2
import pdb 
import numpy as np
from utils.utils import *


img = cv2.imread("assets/src.png")
lmks = get_lmk(img)

h,w,_ = img.shape
lmks = add_edge(lmks,h,w)
# lmks = np.array(lmks) * 10
triangle = getTriangleList(lmks)
np.save("assets/index.npy",triangle)
img = draw_triset(img,lmks,triangle)


cv2.imwrite("triangle.png",img)







       