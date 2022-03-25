import glfw
from OpenGL.GL import *  # pylint: disable=W0614
from OpenGL.GLU import *  # pylint: disable=W0614
import numpy as np
import glm
from utils.shaderLoader import Shader

class BaseShader:
    def __init__(self,vs_path,fs_path,**kwargs):
        self.shader = Shader()
        self.shader.initShaderFromGLSL([vs_path],[fs_path])
        for key,val in kwargs.items():
            setattr(self,key,val)

        self.stand_att1 = [
            -1.0, 1.0, 0.0,  # Position 0
            -1.0, -1.0, 0.0,  # Position 1
            1.0, -1.0, 0.0,  # Position 2
            1.0, 1.0, 0.0,  # Position 3
        ]

        self.stand_att2 = [
            0.0, 1.0,  # TexCoord 0
            0.0, 0.0,  # TexCoord 1
            1.0, 0.0,  # TexCoord 2
            1.0, 1.0  # TexCoord 3
        ]


        

        self.stand_index = [0, 1, 2, 0, 2, 3]
        # self.stand_index = [0, 1,  3]


    def build_shader(self,width,height,outFboId):
        glUseProgram(self.shader.program)

        glBindFramebuffer(GL_FRAMEBUFFER, outFboId)
        glViewport(0, 0, width, height)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)


    # 将坐标传输到gpu上
    def transform_axis(self,att1,att2,index):
        self.vertexbuffer  = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER,self.vertexbuffer)
        glBufferData(GL_ARRAY_BUFFER,len(att1)*4,(GLfloat * len(att1))(*att1),GL_STATIC_DRAW)

        self.coordBuffer  = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER,self.coordBuffer)
        glBufferData(GL_ARRAY_BUFFER,len(att2)*4,(GLfloat * len(att2))(*att2),GL_STATIC_DRAW)

        
        indicesbuffer  = glGenBuffers(1)
        self.indicesSize = len(index)		
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,indicesbuffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,self.indicesSize*2,(GLushort * self.indicesSize)(*index),GL_STATIC_DRAW)

       

    # 绑定纹理，常量
    def get_uniform(self,name):
        return glGetUniformLocation(self.shader.program, name)

    # 传输常量
    def bind_constant(self,location,val):
        try:
            glUniform1f(location,val)
        except:
            glUniform1i(location,val)

    # 传输纹理
    def bind_tex(self,location,val,textureid):
        glActiveTexture(GL_TEXTURE0+val)
        glUniform1i(location, val)
        glBindTexture(GL_TEXTURE_2D, textureid)

    # 传入顶点
    def bind_axis(self):
        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexbuffer)
        glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,12,None)
        # glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,0,None)

        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.coordBuffer)
        glVertexAttribPointer(1,2,GL_FLOAT,GL_FALSE,8,None)

    # 绑定图片
    def bind_img(self,img,texture):
        
       
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.shape[1], img.shape[0], 0, GL_RGB, GL_UNSIGNED_BYTE,
                     img.data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S,GL_CLAMP_TO_EDGE );
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,GL_CLAMP_TO_EDGE);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,GL_LINEAR);

    # 输出
    def show(self,width,height,returnImage):
        gl_err = glGetError()
        if gl_err != 0:
            print(f'draw glGetError():{gl_err}')

        

        glDrawElements(GL_TRIANGLES, self.indicesSize, GL_UNSIGNED_SHORT, None)

        # Read back the created pixels:
        glFinish()
        if returnImage:
            data = glReadPixelsub(0, 0, width, height, OpenGL.GL.GL_RGBA)
            img = np.frombuffer(data, dtype=np.uint8).reshape(
                height, width, 4)
            return img
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        return None
    


    

    