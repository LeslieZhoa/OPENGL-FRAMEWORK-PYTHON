#version 330 core 
uniform sampler2D varImageTex;

in vec2 textureCoord;

in vec4 texBlurShift1;
in vec4 texBlurShift2;
in vec4 texBlurShift3;
in vec4 texBlurShift4;
layout(location = 0) out vec4 FragColor;

void main()
{
    vec4 color = texture(varImageTex, textureCoord);
    float sum = color.a;
    sum += texture(varImageTex, texBlurShift1.xy).a;
    sum += texture(varImageTex, texBlurShift1.zw).a;
    sum += texture(varImageTex, texBlurShift2.xy).a;
    sum += texture(varImageTex, texBlurShift2.zw).a;
    sum += texture(varImageTex, texBlurShift3.xy).a;
    sum += texture(varImageTex, texBlurShift3.zw).a;
    sum += texture(varImageTex, texBlurShift4.xy).a;
    sum += texture(varImageTex, texBlurShift4.zw).a;
    
    //rgb channel for smoothSrcImage, alpha channel for smoothVarImage
    FragColor = vec4(color.rgb, sum * 0.1111);
}