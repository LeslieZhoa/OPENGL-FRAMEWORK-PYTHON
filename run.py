import glfw
from OpenGL.GL import *  # pylint: disable=W0614
from OpenGL.GLU import *  # pylint: disable=W0614

import glm
from matplotlib.pyplot import draw
from utils.utils import *
from utils.shaderLoader import Shader
import numpy as np
import cv2
import sys
import pdb

from shader_function.blur1 import Blur1
from shader_function.draw import Draw

from shader_function.lut3 import Lut3

from shader_function.baseEffect import BaseEffect






class Color1(BaseEffect):
    def __init__(self,width,height):
        
       super().__init__(width,height)
    

    def create_fbo_and_textures(self, width, height):

        # super().__create_fbo_and_textures(width, height)
        fbo = GLuint()
        glGenFramebuffers(1, fbo)
        texture = glGenTextures(8)

        self.bind_blank(width,height,texture[1])
        self.bind_blank(width//2,height//2,texture[2])
        self.bind_blank(width,height,texture[3])
        self.bind_blank(width,height,texture[4])
        self.bind_blank(width,height,texture[5])
        self.bind_blank(width,height,texture[6])
        
        return (fbo, texture)

    def init(self):
        super().init()
        self.blur = Blur1()
        
        self.lut3 = Lut3()

        self.draw = Draw()
        

    def update(self, img,lmks):
        
        
        self.checkwindow(img)
        self.fbo, self.texture = self.create_fbo_and_textures(self.width, self.height)

        raw_img = img.copy()
        
        
        #texture[0]存储原始图片输入
        # pdb.set_trace()
        self.bind_img(self.width,self.height,self.texture[0],raw_img)

        out = self.do_shader(self.texture[1],self.texture[0],self.draw,False,lmks) 
        
        out = self.do_shader(self.texture[2],self.texture[1],self.blur,False)

        out = self.do_shader(self.texture[3],self.texture[2],self.lut3,True)

        out_img = cv2.cvtColor(out, cv2.COLOR_RGBA2BGR)
      
        glfw.poll_events()

        glfw.terminate()
        ### img_comic is RGBA
        return out_img




if __name__ == "__main__":
    img_path = "./assets/src.png"
    
    src_lmk = get_lmk(img_path)

    target_lmk = convert_lmk(src_lmk)

    index = np.load("assets/index.npy").reshape(-1).tolist()

    img = cv2.cvtColor(cv2.imread(img_path),cv2.COLOR_BGR2RGBA)
    h,w,_ = img.shape
    # pdb.set_trace()
    src_lmk = add_edge(src_lmk,h,w)
    # target_lmk = add_edge(target_lmk,h,w)
    target_lmk = np.concatenate([ target_lmk,src_lmk[81:]],0)

    
    src_lmk = src_lmk / np.array([w,h])
    target_lmk = (target_lmk / np.array([w,h]) - 0.5) * 2

    target_lmk = np.concatenate([target_lmk,np.zeros((target_lmk.shape[0],1))],-1)
    color_engine = Color1(h,w)
    color_engine.init()
    out_img = color_engine.update(img,[target_lmk.reshape(-1).tolist(),src_lmk.reshape(-1).tolist(),index])
    cv2.imwrite("res.png",out_img)
