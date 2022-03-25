#version 330 core 
uniform sampler2D inputImageTexture1;
in vec2 textureCoordinate;
in vec4 textureShift_1;
in vec4 textureShift_2;
in vec4 textureShift_3;
in vec4 textureShift_4;
layout(location = 0) out vec4 FragColor;
void main()
{
    vec3 sum = texture(inputImageTexture1, textureCoordinate).rgb;
    sum += texture(inputImageTexture1, textureShift_1.xy).rgb;
    sum += texture(inputImageTexture1, textureShift_1.zw).rgb;
    sum += texture(inputImageTexture1, textureShift_2.xy).rgb;
    sum += texture(inputImageTexture1, textureShift_2.zw).rgb;
    sum += texture(inputImageTexture1, textureShift_3.xy).rgb;
    sum += texture(inputImageTexture1, textureShift_3.zw).rgb;
    sum += texture(inputImageTexture1, textureShift_4.xy).rgb;
    sum += texture(inputImageTexture1, textureShift_4.zw).rgb;
    
    FragColor = vec4(sum.rgb * 0.1111, 1.0);
    // FragColor = vec4(sum.rgb,1.0);

}
