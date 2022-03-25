## OPENGL-FRAMEWORK-PYTHON
[English version](https://github.com/LeslieZhoa/OPENGL-FRAMEWORK-PYTHON/blob/main/ReadMe.md)<br>
[中文版本](https://github.com/LeslieZhoa/OPENGL-FRAMEWORK-PYTHON/blob/main/ReadMe_chinese.md)
### Introduce
This is a convenient and extensible Python OpenGL framework. You can easily refer to the example shader to realize the custom rendering function
### Environmental preparation
- Dlib is installed for face key point detection. It is recommended to search and install the source code, which is not easy to make mistakes
- `pip install -r requirements.txt`Install OpenGL related environment<br>
if Unable to load/find OpenGL on MacOS refer to [Link](https://github.com/PixarAnimationStudios/USD/issues/1372)
### File Structure
- assets
  - Storage path of various LUT pictures, indexes, etc
- shader
  - Shader script, if you want to achieve their own rendering, you can refer to any .vs and .fs
- shader_function
  - Call the function of shader and incoming data. If you want to realize your own rendering, you can refer to any .py
- get_index.py
  - Get face key points and triangulation index according to Dlib，thank @codeniko for providing the [key points model](https://github.com/codeniko/shape_predictor_81_face_landmarks) including forehead
- run.py
  - Main file, main functions: deformation + blur + filter
### 运行
- `python get_index.py`Get face key points and triangulation index according to Dlib
- `python run.py`make assets/src.png Deformation + blur + filter to res.png
