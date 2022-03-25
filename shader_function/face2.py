import glfw
from OpenGL.GL import *  # pylint: disable=W0614
from OpenGL.GLU import *  # pylint: disable=W0614
import numpy as np
import glm
from utils.shaderLoader import Shader
from shader_function.base_shader import BaseShader
import cv2
import pdb

class Face2(BaseShader):
    def __init__(self,vs_path="shader/color2.vs",fs_path="shader/color2.fs",widthOffset=0.0013888889,
                heightOffset=7.8125e-7,useMask=1,defaultMaskValue=0.6,blurAlpha=0,sharpen=0,
                eyeDetailIntensity=0.6):
        super().__init__(vs_path="shader/color2.vs",fs_path="shader/color2.fs",widthOffset=0.0013888889,
                heightOffset=7.8125e-7,useMask=1,defaultMaskValue=0.6,blurAlpha=0,sharpen=0,
                eyeDetailIntensity=0.6)
        
        mask1 = cv2.cvtColor(cv2.imread("assets/mask1.png"),cv2.COLOR_BGR2RGB)
        mask2 = cv2.cvtColor(cv2.imread("assets/eye.png"),cv2.COLOR_BGR2RGB)
        self.texture = glGenTextures(2)
        self.bind_img(mask1,self.texture[0])
        self.bind_img(mask2,self.texture[1])
        self.att2 = np.load("assets/stand_lmk.npy").reshape(-1).tolist()
        self.vIndices = np.load("assets/index.npy").reshape(-1).tolist()

    def runFbo(self, width, height, textureId,outFboId,returnImage,att1):
        # 绑定纹理，常量
        self.srcImageTex = self.get_uniform("srcImageTex")
        self.blurImageTex = self.get_uniform("blurImageTex")
        self.eyeMaskTexture = self.get_uniform("eyeMaskTexture")
        self.beautyMaskTexture = self.get_uniform("beautyMaskTexture")

        self.l1 = self.get_uniform("widthOffset")
        self.l0 = self.get_uniform("heightOffset")
        self.l2 = self.get_uniform("useMask");
        
        self.l3 = self.get_uniform("defaultMaskValue");

        self.l4 = self.get_uniform("blurAlpha");
        
        self.l5 = self.get_uniform("sharpen");
        self.l6 = self.get_uniform("eyeDetailIntensity");

        # 绑定坐标
        # pdb.set_trace()
        self.transform_axis(att1[0],att1[1],self.vIndices)

        self.build_shader(width,height,outFboId)

        # 传入常量
        self.bind_constant(self.l1,self.widthOffset)
        self.bind_constant(self.l0,self.heightOffset)

        self.bind_constant(self.l2,self.useMask)
        self.bind_constant(self.l3,self.defaultMaskValue)
        self.bind_constant(self.l4,self.blurAlpha)
        self.bind_constant(self.l5,self.sharpen)
        self.bind_constant(self.l6,self.eyeDetailIntensity)
        
        # 传入纹理
        self.bind_tex(self.srcImageTex,0,textureId[0])
        self.bind_tex(self.blurImageTex,1,textureId[1])
        self.bind_tex(self.beautyMaskTexture,2,self.texture[0])
        self.bind_tex(self.eyeMaskTexture,3,self.texture[1])

        # 传入顶点
        self.bind_axis()

        return self.show(width,height,returnImage)
    def __del__(self):
        
            
        glDeleteTextures(self.texture)



