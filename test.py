import dlib
import cv2
import pdb 
import numpy as np
from utils.utils import *


img = cv2.imread("assets/src.png")
src_lmk = get_lmk(img)

target_lmk = convert_lmk(src_lmk)

index = np.load("assets/index.npy")

h,w,_ = img.shape

src_lmk = add_edge(src_lmk,h,w)
target_lmk = add_edge(target_lmk,h,w)

img1 = img.copy()

img = draw_triset(img,src_lmk,index)

img1 = draw_triset(img1,target_lmk,index)

cv2.imwrite("h1.png",img)
cv2.imwrite("h2.png",img1)
