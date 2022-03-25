#version 330 core 
uniform sampler2D srcImageTex;

in vec2 textureCoord;

in vec4 texBlurShift1;
in vec4 texBlurShift2;
in vec4 texBlurShift3;
in vec4 texBlurShift4;
layout(location = 0) out vec4 FragColor;

void main()
{
    vec3 sum = texture(srcImageTex, textureCoord).rgb;
    sum += texture(srcImageTex, texBlurShift1.xy).rgb;
    sum += texture(srcImageTex, texBlurShift1.zw).rgb;
    sum += texture(srcImageTex, texBlurShift2.xy).rgb;
    sum += texture(srcImageTex, texBlurShift2.zw).rgb;
    sum += texture(srcImageTex, texBlurShift3.xy).rgb;
    sum += texture(srcImageTex, texBlurShift3.zw).rgb;
    sum += texture(srcImageTex, texBlurShift4.xy).rgb;
    sum += texture(srcImageTex, texBlurShift4.zw).rgb;
    
    FragColor = vec4(sum * 0.1111, 1.0);
}
