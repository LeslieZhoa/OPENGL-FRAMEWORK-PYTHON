import glfw
from OpenGL.GL import *  # pylint: disable=W0614
from OpenGL.GLU import *  # pylint: disable=W0614
import numpy as np
import glm
from utils.shaderLoader import Shader
from shader_function.base_shader import BaseShader
import cv2

class Lut2(BaseShader):
    def __init__(self,vs_path="shader/lut2.vs",fs_path="shader/lut2.fs",clearIntensity=0.16):
        super().__init__(vs_path="shader/lut2.vs",fs_path="shader/lut2.fs",clearIntensity=0.16)
        lut1 = cv2.cvtColor(cv2.flip(cv2.imread("assets/lut2.png"),0),cv2.COLOR_BGR2RGB)
        self.texture = glGenTextures(1)
        self.bind_img(lut1,self.texture)

    def runFbo(self, width, height, textureId, outFboId,returnImage,att1):
        # 绑定纹理，常量
        self.inputTex = self.get_uniform("inputTex")
        self.lutImageForClear = self.get_uniform("lutImageForClear")

        self.l0 = self.get_uniform("clearIntensity")
        # 绑定坐标
        self.transform_axis(self.stand_att1,self.stand_att2,self.stand_index)

        self.build_shader(width,height,outFboId)

        # 传入常量
        self.bind_constant(self.l0,self.clearIntensity)
        
        # 传入纹理
        self.bind_tex(self.inputTex,0,textureId)
        self.bind_tex(self.lutImageForClear,1,self.texture)

        # 传入顶点
        self.bind_axis()

        return self.show(width,height,returnImage)
    


