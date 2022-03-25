import glfw
from OpenGL.GL import *  # pylint: disable=W0614
from OpenGL.GLU import *  # pylint: disable=W0614
import numpy as np
import glm
from utils.shaderLoader import Shader
from shader_function.base_shader import BaseShader
import cv2

class Lut3(BaseShader):
    def __init__(self,vs_path="shader/lut3.vs",fs_path="shader/lut3.fs",leftIntensity=1.0,rightIntensity=1.0,
                mposition=1.0):
        super().__init__(vs_path="shader/lut3.vs",fs_path="shader/lut3.fs",leftIntensity=1.0,rightIntensity=1.0,
                mposition=1.0)
        lut1 = cv2.cvtColor(cv2.flip(cv2.imread("assets/lut3-1.png"),0),cv2.COLOR_BGR2RGB)
        lut2 = cv2.cvtColor(cv2.flip(cv2.imread("assets/lut3-2.png"),0),cv2.COLOR_BGR2RGB)
        self.texture = glGenTextures(2)
        self.bind_img(lut1,self.texture[0])
        self.bind_img(lut2,self.texture[1])

    def runFbo(self, width, height, textureId, outFboId,returnImage,att1):
        # 绑定纹理，常量
        self.inputImageTexture1 = self.get_uniform("inputImageTexture1")
        self.inputImageTexture2 = self.get_uniform("inputImageTexture2")
        self.inputImageTexture3 = self.get_uniform("inputImageTexture3")
        

        self.l0 = self.get_uniform("leftIntensity");
        
        self.l1 = self.get_uniform("rightIntensity");
        
        self.l2 = self.get_uniform("mposition");
        # 绑定坐标
        self.transform_axis(self.stand_att1,self.stand_att2,self.stand_index)

        self.build_shader(width,height,outFboId)

        # 传入常量
        self.bind_constant(self.l0,self.leftIntensity)
        self.bind_constant(self.l1,self.rightIntensity)
        self.bind_constant(self.l2,self.mposition)
        
        # 传入纹理
        self.bind_tex(self.inputImageTexture1,0,textureId)
        self.bind_tex(self.inputImageTexture2,1,self.texture[0])
        self.bind_tex(self.inputImageTexture3,2,self.texture[1])

        # 传入顶点
        self.bind_axis()

        return self.show(width,height,returnImage)
    def __del__(self):
       
            
        glDeleteTextures(self.texture)



