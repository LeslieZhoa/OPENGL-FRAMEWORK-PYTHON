## OPENGL-FRAMEWORK-PYTHON
### 介绍
这是一个方便扩展的python版opengl框架，可以很轻松的参考示例shader来实现自定义的渲染功能
### 环境准备
- 安装dlib，用于人脸关键点检测，建议搜索使用源码安装，不易出错
- `pip install -r requirements.txt`安装opengl相关环境<br>
如果macos出错Unable to load/find OpenGL on MacOS 参考[这里](https://github.com/PixarAnimationStudios/USD/issues/1372)
### 文件结构
- assets
  - 各种lut图片，index等的存放路径
- shader
  - shader的脚本，如果要实现自己的渲染可参考任意.vs和.fs
- shader_function
  - 调用shader以及传入数据的功能，如果要实现自己的渲染可参考任意.py
- get_index.py
  - 根据dlib获取人脸关键点和三角剖分index，感谢@codeniko 提供的包括额头关键点的[人脸关键点检测模型](https://github.com/codeniko/shape_predictor_81_face_landmarks)
- run.py
  - 主文件，主要功能形变+模糊+滤镜
### 运行
- `python get_index.py`根据dlib获取人脸关键点和三角剖分index
- `python run.py`将assets/src.png形变+模糊+滤镜,生成res.png
