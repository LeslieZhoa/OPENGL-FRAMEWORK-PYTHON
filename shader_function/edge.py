import glfw
from OpenGL.GL import *  # pylint: disable=W0614
from OpenGL.GLU import *  # pylint: disable=W0614
import numpy as np
import glm
from utils.shaderLoader import Shader
from shader_function.base_shader import BaseShader

class Edge(BaseShader):
    def __init__(self,vs_path="shader/edge.vs",fs_path="shader/edge.fs",weightoffset=0.0030864198,heightoffset=0.0):
        super().__init__(vs_path="shader/edge.vs",fs_path="shader/edge.fs",weightoffset=0.0030864198,heightoffset=0.0)
        

    def runFbo(self, width, height, textureId,outFboId,returnImage,att1):
        # 绑定纹理，常量
        self.srcImageTex = self.get_uniform("srcImageTex")
        self.blurImageTex = self.get_uniform("blurImageTex")
        self.l1 = self.get_uniform("texBlurHeightOffset")
        self.l0 = self.get_uniform("texBlurWidthOffset")
        # 绑定坐标
        self.transform_axis(self.stand_att1,self.stand_att2,self.stand_index)

        self.build_shader(width//2,height//2,outFboId)

        # 传入常量
        self.bind_constant(self.l1,self.heightoffset)
        self.bind_constant(self.l0,self.weightoffset)
        
        # 传入纹理
        self.bind_tex(self.srcImageTex,0,textureId[0])
        self.bind_tex(self.blurImageTex,1,textureId[1])

        # 传入顶点
        self.bind_axis()

        return self.show(width//2,height//2,returnImage)



