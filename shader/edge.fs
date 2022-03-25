#version 330 core 
in vec2 textureCoord;

in vec4 texBlurShift1;
in vec4 texBlurShift2;
in vec4 texBlurShift3;
in vec4 texBlurShift4;

uniform sampler2D srcImageTex;
uniform sampler2D blurImageTex;
layout(location = 0) out vec4 FragColor;

void main()
{
    //firstly, boxblur src image horizontally
    vec3 sum = texture(blurImageTex, textureCoord).rgb;
    sum += texture(blurImageTex, texBlurShift1.xy).rgb;
    sum += texture(blurImageTex, texBlurShift1.zw).rgb;
    sum += texture(blurImageTex, texBlurShift2.xy).rgb;
    sum += texture(blurImageTex, texBlurShift2.zw).rgb;
    sum += texture(blurImageTex, texBlurShift3.xy).rgb;
    sum += texture(blurImageTex, texBlurShift3.zw).rgb;
    sum += texture(blurImageTex, texBlurShift4.xy).rgb;
    sum += texture(blurImageTex, texBlurShift4.zw).rgb;
    
    vec3 meanColor = sum * 0.1111;
    
    vec3 inColor = texture(srcImageTex, textureCoord).rgb;
    
    vec3 diffColor = (inColor - meanColor) * 7.07;
    diffColor = min(diffColor * diffColor, 1.0);
    
    FragColor = vec4(meanColor, (diffColor.r + diffColor.g + diffColor.b) * 0.3333);
    // FragColor = vec4(meanColor,1);
    // FragColor = vec4(diffColor,1);
}