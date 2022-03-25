#version 330 core 
in vec2 textureCoordinate;
in vec2 textureCoordinate2;
uniform sampler2D inputImageTexture1;
uniform sampler2D inputImageTexture2;
layout(location = 0) out vec4 FragColor;
void main()
{
    vec3 iColor = texture(inputImageTexture1, textureCoordinate).rgb;
    vec3 meanColor = texture(inputImageTexture2, textureCoordinate2).rgb;
    vec3 diffColor = (iColor - meanColor) * 7.07;
    diffColor = min(diffColor * diffColor, 1.0);
    FragColor = vec4(diffColor, 1.0);
}
