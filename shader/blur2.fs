#version 330 core 
uniform sampler2D inputImageTexture;
in vec2 textureCoordinate;
in vec4 textureShift_1;
in vec4 textureShift_2;
layout(location = 0) out vec4 FragColor;
void main()
{
    vec3 sum = texture(inputImageTexture, textureCoordinate).rgb;
    sum += texture(inputImageTexture, textureShift_1.xy).rgb;
    sum += texture(inputImageTexture, textureShift_1.zw).rgb;
    sum += texture(inputImageTexture, textureShift_2.xy).rgb;
    sum += texture(inputImageTexture, textureShift_2.zw).rgb;
    sum = sum * 0.2;
    FragColor = vec4(sum, 1.0);
}
