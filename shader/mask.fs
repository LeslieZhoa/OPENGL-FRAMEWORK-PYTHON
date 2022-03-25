#version 330 core 

in vec2 maskTexCoord;
uniform sampler2D inputImageMaskTexture;
layout(location = 0) out vec4 FragColor;
void main()
{
    vec4 maskColor = texture(inputImageMaskTexture, maskTexCoord);
    FragColor = vec4(maskColor.rgb, 1.0);
}