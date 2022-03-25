import glfw
from OpenGL.GL import *  # pylint: disable=W0614
from OpenGL.GLU import *  # pylint: disable=W0614
import numpy as np
import glm
from utils.shaderLoader import Shader
from shader_function.base_shader import BaseShader

class Contract(BaseShader):
    def __init__(self,vs_path="shader/high_contrast.vs",fs_path="shader/high_contrast.fs"):
        super().__init__(vs_path="shader/high_contrast.vs",fs_path="shader/high_contrast.fs")
        

    def runFbo(self, width, height, textureId, outFboId,returnImage,att1):
        # 绑定纹理，常量
        self.samplerLoc_img = self.get_uniform("inputImageTexture1")
        self.samplerLoc_lut = self.get_uniform("inputImageTexture2");
        
        # 绑定坐标
        self.transform_axis(self.stand_att1,self.stand_att2,self.stand_index)

        self.build_shader(width//2,height//2,outFboId)

       
        
        # 传入纹理
        self.bind_tex(self.samplerLoc_img,0,textureId[0])
        self.bind_tex(self.samplerLoc_img,1,textureId[1])

        # 传入顶点
        self.bind_axis()

        return self.show(width//2,height//2,returnImage)



