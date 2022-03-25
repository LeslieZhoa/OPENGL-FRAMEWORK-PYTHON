import glfw
from OpenGL.GL import *  # pylint: disable=W0614
from OpenGL.GLU import *  # pylint: disable=W0614
import numpy as np
import glm
from utils.shaderLoader import Shader
from shader_function.base_shader import BaseShader
import cv2

class Deepen(BaseShader):
    def __init__(self,vs_path="shader/color1.vs",fs_path="shader/color1.fs",
                weightoffset=0,heightoffset=0.00260417,
                blurAlpha1=1.0,blurAlpha2=0.1,sharpen=0.11):
        super().__init__(vs_path="shader/color1.vs",fs_path="shader/color1.fs",
                weightoffset=0,heightoffset=0.00260417,
                blurAlpha1=1.0,blurAlpha2=0.1,sharpen=0.11)

        face_mask = cv2.cvtColor(cv2.imread("assets/12-mask.png"),cv2.COLOR_BGR2RGB)
        lut = cv2.cvtColor(cv2.flip(cv2.imread("assets/12-lut.png"),0),cv2.COLOR_BGR2RGB)
        lut_mask = cv2.cvtColor(cv2.imread("assets/12-lut_mask.png"),cv2.COLOR_BGR2RGB)
        self.texture = glGenTextures(3)
        self.bind_img(face_mask,self.texture[0])
        self.bind_img(lut,self.texture[1])
        self.bind_img(lut_mask,self.texture[2])
        self.att2 = np.load("assets/stand_lmk.npy").reshape(-1).tolist()
        self.vIndices = np.load("assets/index.npy").reshape(-1).tolist()

        

    def runFbo(self, width, height, textureId, outFboId,returnImage,att1):
        # 绑定纹理，常量
        self.srcTex = self.get_uniform("srcTex");
        self.meanBlur = self.get_uniform("meanBlurTex");
        self.varTex = self.get_uniform("variantTex");
        self.faceTex = self.get_uniform("faceMaskTex");
        self.lutTex = self.get_uniform("lutTex");
        self.lutMaskTex = self.get_uniform("lutMaskTex");
        l1 = self.get_uniform("widthOffset");
       
        l0 = self.get_uniform("heightOffset");
       

        l4 = self.get_uniform("blurAlpha1");
      
        l5 = self.get_uniform("blurAlpha2");

        l6 = self.get_uniform("sharpen");
        
        
        
        # 绑定坐标
        self.transform_axis(att1,self.att2,self.vIndices)

        self.build_shader(width,height,outFboId)

       
        
         # 传入常量
        self.bind_constant(l1,self.weightoffset)
        self.bind_constant(l0,self.heightoffset)

        
        self.bind_constant(l4,self.blurAlpha1)
        self.bind_constant(l5,self.blurAlpha2)
        self.bind_constant(l6,self.sharpen)
        
        # 传入纹理
        self.bind_tex(self.srcTex,0,textureId[0])
        self.bind_tex(self.meanBlur,1,textureId[1])
        self.bind_tex(self.varTex,2,textureId[2])
        self.bind_tex(self.faceTex,3,self.texture[0])
        self.bind_tex(self.lutTex,4,self.texture[1])
        self.bind_tex(self.lutMaskTex,5,self.texture[2])

        # 传入顶点
        self.bind_axis()

        return self.show(width,height,returnImage)

    def __del__(self):
        
            
        glDeleteTextures(self.texture)



