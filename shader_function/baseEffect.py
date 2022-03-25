import glfw
from OpenGL.GL import *  # pylint: disable=W0614
from OpenGL.GLU import *  # pylint: disable=W0614
import numpy as np
import glm
from utils.shaderLoader import Shader
from shader_function.base_shader import BaseShader
import cv2

class BaseEffect:
    def __init__(self,width,height):
        
        self.width = width
        self.height = height

        if not glfw.init():
            return
        glfw.window_hint(glfw.SAMPLES,4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR,3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR,3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT,1)
        glfw.window_hint(glfw.OPENGL_PROFILE,glfw.OPENGL_CORE_PROFILE)

        # Create a windowed mode window and its OpenGL context
        self.window = glfw.create_window(324,576, "Hello World", None, None)
        if not self.window:
            glfw.terminate()
            return

        # Make the window's context current
        glfw.make_context_current(self.window)
        self.fbo = None
        self.texture = None
    
    def bind_blank(self,width,height,texture):
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S,GL_CLAMP_TO_EDGE );
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,GL_CLAMP_TO_EDGE);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,GL_LINEAR);
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width,
                     height, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)

    def bind_img(self,width,height,texture,img):
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S,GL_CLAMP_TO_EDGE );
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,GL_CLAMP_TO_EDGE);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,GL_LINEAR);
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width,
                     height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img.data)

    def create_fbo_and_textures(width, height):
        return None,None
        

    def init(self):
        glClearColor(0.0,0,0.4,0)
        # glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        

        vertex = glGenVertexArrays(1) # pylint: disable=W0612
        glBindVertexArray(vertex)
        
        self.fbo, self.texture = self.create_fbo_and_textures(self.width, self.height)
    def do_shader(self,save_texture,input_texture,shader_func,returnImage,att1=None):
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        glFramebufferTexture2D(
            GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D,save_texture,0)
        status = glCheckFramebufferStatus(GL_FRAMEBUFFER)
        outblur1 = shader_func.runFbo(self.width, self.height,input_texture,self.fbo,returnImage,att1)
        return outblur1

    def checkwindow(self,img):
        if self.width != img.shape[1] or self.height != img.shape[0]:
            self.width = img.shape[1]
            self.height = img.shape[0]
            glfw.set_window_size(self.window, self.width, self.height)
        if self.fbo is not None:
            glDeleteFramebuffers(1, self.fbo)
        if self.texture is not None:
            glDeleteTextures(self.texture)
  
   

        

        
        
        


        
