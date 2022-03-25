#version 330 core 

precision highp float;

in vec2 textureCoordinate;
uniform sampler2D inputImageTexture;
layout(location = 0) out vec4 FragColor;

void main(void)
{
    FragColor = texture(inputImageTexture, textureCoordinate);
}
