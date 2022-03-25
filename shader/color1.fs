#version 330 core 
in vec2 texUV;
in vec2 srcUV;

uniform sampler2D srcTex;
uniform sampler2D meanBlurTex;
uniform sampler2D variantTex;
uniform sampler2D faceMaskTex;
uniform float blurAlpha1; 
uniform float blurAlpha2; // bg blur
uniform float sharpen;
uniform sampler2D lutTex;
uniform sampler2D lutMaskTex;

in vec4 textureShift_1;
in vec4 textureShift_2;
in vec4 textureShift_3;
in vec4 textureShift_4;

const float levelRangeInv = 1.02657;
const float levelBlack = 0.0258820;
const float alpha = 0.7;
layout(location = 0) out vec4 FragColor;

void main()
{
    vec3 iColor = texture(srcTex, srcUV).rgb;
    vec3 meanColor = texture(meanBlurTex, srcUV).rgb;
    vec3 varColor = texture(variantTex, srcUV).rgb;
    
    float theta = 0.1;
    float p = clamp((min(iColor.r, meanColor.r - 0.1) - 0.2) * 4.0, 0.0, 1.0);
    float meanVar = (varColor.r + varColor.g + varColor.b) / 3.0;
    float kMin;
    vec3 resultColor;
    float faceMask = texture(faceMaskTex, texUV).r;
    float blurAlpha = mix(blurAlpha2, blurAlpha1, faceMask);
    kMin = (1.0 - meanVar / (meanVar + theta)) * p * blurAlpha;
    resultColor = mix(iColor.rgb, meanColor.rgb, kMin);
    
    float hPass = iColor.g-meanColor.g+0.5;
    float flag = step(0.5, hPass);
    vec3 color = mix(max(vec3(0.0), (2.0*hPass + resultColor - 1.0)), min(vec3(1.0), (resultColor + 2.0*hPass - 1.0)), flag);
    vec3 colorEPM = mix(resultColor.rgb, color.rgb, sharpen);

    vec3 whiteColor = clamp(colorEPM, 0., 1.).rgb;
    float blueColor_custom = whiteColor.b * 63.0;
    vec2 quad1_custom;
    quad1_custom.y = floor(floor(blueColor_custom) / 8.0);
    quad1_custom.x = floor(blueColor_custom) - (quad1_custom.y * 8.0);
    vec2 quad2_custom;
    quad2_custom.y = floor(ceil(blueColor_custom) / 8.0);
    quad2_custom.x = ceil(blueColor_custom) - (quad2_custom.y * 8.0);
    vec2 texPos1_custom;
    texPos1_custom.x = (quad1_custom.x * 1.0 / 8.0) + 0.5 / 512.0 + ((1.0 / 8.0 - 1.0 / 512.0) * whiteColor.r);
    texPos1_custom.y = (quad1_custom.y * 1.0 / 8.0) + 0.5 / 512.0 + ((1.0 / 8.0 - 1.0 / 512.0) * whiteColor.g);
    vec2 texPos2_custom;
    texPos2_custom.x = (quad2_custom.x * 1.0 / 8.0) + 0.5 / 512.0 + ((1.0 / 8.0 - 1.0 / 512.0) * whiteColor.r);
    texPos2_custom.y = (quad2_custom.y * 1.0 / 8.0) + 0.5 / 512.0 + ((1.0 / 8.0 - 1.0 / 512.0) * whiteColor.g);
    vec3 newColor1 = texture(lutTex, texPos1_custom).rgb;
    vec3 newColor2 = texture(lutTex, texPos2_custom).rgb;
    // vec3 newColor2 = texture(lutTex, textureShift_2).rgb;

    float lutAlpha = texture(lutMaskTex, texUV).r;
    FragColor = vec4(mix(colorEPM.rgb, mix(newColor1, newColor2, fract(blueColor_custom)), lutAlpha), 1.);
    // FragColor = vec4(colorEPM.rgb,1);
    // FragColor = vec4(mix(newColor1, newColor2, fract(blueColor_custom)), 1.);
}
