import glfw
from OpenGL.GL import *  # pylint: disable=W0614
from OpenGL.GLU import *  # pylint: disable=W0614
import numpy as np
import glm
from utils.shaderLoader import Shader
from shader_function.base_shader import BaseShader

class Blur4(BaseShader):
    def __init__(self,vs_path="shader/blur4.vs",fs_path="shader/blur4.fs",weightoffset=0.0,heightoffset=0.0017361111):
        super().__init__(vs_path="shader/blur4.vs",fs_path="shader/blur4.fs",weightoffset=0.0,heightoffset=0.0017361111)
        

    def runFbo(self, width, height, textureId,outFboId,returnImage,att1):
        # 绑定纹理，常量
        self.samplerLoc_img = self.get_uniform("varImageTex")
        self.l1 = self.get_uniform("texBlurHeightOffset")
        self.l0 = self.get_uniform("texBlurWidthOffset")
        # 绑定坐标
        self.transform_axis(self.stand_att1,self.stand_att2,self.stand_index)

        self.build_shader(width//2,height//2,outFboId)

        # 传入常量
        self.bind_constant(self.l1,self.heightoffset)
        self.bind_constant(self.l0,self.weightoffset)
        
        # 传入纹理
        self.bind_tex(self.samplerLoc_img,0,textureId)

        # 传入顶点
        self.bind_axis()

        return self.show(width//2,height//2,returnImage)



