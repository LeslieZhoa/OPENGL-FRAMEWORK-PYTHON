import glfw
from OpenGL.GL import *  # pylint: disable=W0614
from OpenGL.GLU import *  # pylint: disable=W0614
import numpy as np
import glm
from utils.shaderLoader import Shader
from shader_function.base_shader import BaseShader
import cv2

class Eye(BaseShader):
    def __init__(self,vs_path="shader/eye_light.vs",fs_path="shader/eye_light.fs",intensity=0.6,eyeDetailIntensity=1.0,removePouchIntensity=1.0,
                removeNasolabialFoldsIntensity=0.35):
        super().__init__(vs_path="shader/eye_light.vs",fs_path="shader/eye_light.fs",intensity=0.6,eyeDetailIntensity=1.0,removePouchIntensity=1.0,
                removeNasolabialFoldsIntensity=0.35)

        mask = cv2.cvtColor(cv2.imread("assets/eye.png"),cv2.COLOR_BGR2RGB)
        self.texture = glGenTextures(1)
        self.bind_img(mask,self.texture)
       
        self.att2 = np.load("assets/stand_lmk.npy").reshape(-1).tolist()
        self.vIndices = np.load("assets/index.npy").reshape(-1).tolist()

        

    def runFbo(self, width, height, textureId, outFboId,returnImage,att1):
        # 绑定纹理，常量
        self.inputImageTexture = self.get_uniform("inputImageTexture");
        self.inputScaledTexture = self.get_uniform("inputScaledTexture");
        self.inputScaledBlurTexture = self.get_uniform("inputScaledBlurTexture");
        self.inputImageMaskTexture = self.get_uniform("inputImageMaskTexture");
       
        l1 = self.get_uniform("intensity");
       
        l0 = self.get_uniform("eyeDetailIntensity");
       

        l4 = self.get_uniform("removePouchIntensity");
      
        l5 = self.get_uniform("removeNasolabialFoldsIntensity");
        
        
        
        # 绑定坐标
        self.transform_axis(att1,self.att2,self.vIndices)

        self.build_shader(width,height,outFboId)

       
        
         # 传入常量
        self.bind_constant(l1,self.intensity)
        self.bind_constant(l0,self.eyeDetailIntensity)

        
        self.bind_constant(l4,self.removePouchIntensity)
        self.bind_constant(l5,self.removeNasolabialFoldsIntensity)
       
        
        # 传入纹理
        self.bind_tex(self.inputImageMaskTexture,0,self.texture)
        self.bind_tex(self.inputImageTexture,1,textureId[0])
        self.bind_tex(self.inputScaledTexture,2,textureId[0])
        self.bind_tex(self.inputScaledBlurTexture,3,textureId[1])

        # 传入顶点
        self.bind_axis()

        return self.show(width,height,returnImage)

   



