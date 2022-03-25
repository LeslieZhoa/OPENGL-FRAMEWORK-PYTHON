import glfw
from OpenGL.GL import *  # pylint: disable=W0614
from OpenGL.GLU import *  # pylint: disable=W0614
import numpy as np
import glm
from utils.shaderLoader import Shader
from shader_function.base_shader import BaseShader
import pdb

class Draw(BaseShader):
    def __init__(self,vs_path="shader/draw.vs",fs_path="shader/draw.fs"):
        super().__init__(vs_path="shader/draw.vs",fs_path="shader/draw.fs")
        

    def runFbo(self, width, height, textureId, outFboId,returnImage,lmks):
        # 绑定纹理，常量
        self.samplerLoc_img = self.get_uniform("inputImageTexture")

       
        att1,att2,index = lmks
        
       

        # 绑定坐标
        index = [128,115,120]
        # self.transform_axis(att1,att2,index)
        self.transform_axis(self.stand_att1,self.stand_att2,self.stand_index)
        # glBindFramebuffer(GL_FRAMEBUFFER, outFboId)
        # glDeleteFramebuffers(1,outFboId)
        self.build_shader(width,height,outFboId)

      
        # 传入纹理
        self.bind_tex(self.samplerLoc_img,0,textureId)

        # 传入顶点
        self.bind_axis()

        res = self.show(width,height,returnImage)
        

        return res



