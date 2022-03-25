#version 330 core 
layout(location = 0) in vec3 attPosition;
layout(location = 1) in vec2 attUV;

out vec2 textureCoordinate;
out vec2 textureCoordinate2;

void main(void)
{
    gl_Position = vec4(attPosition, 1.0);
    textureCoordinate = attUV;
    textureCoordinate2 = attUV;
}
