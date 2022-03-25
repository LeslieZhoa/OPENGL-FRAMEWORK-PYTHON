#version 330 core 

in vec2 textureCoord;
in vec2 maskTexCoord;
in vec2 textureShift_1;
in vec2 textureShift_2;
in vec2 textureShift_3;
in vec2 textureShift_4;

uniform sampler2D srcImageTex;
uniform sampler2D blurImageTex;

uniform sampler2D eyeMaskTexture;
uniform sampler2D beautyMaskTexture;

uniform int useMask;
uniform float defaultMaskValue;

uniform float blurAlpha;
uniform float sharpen;
uniform float eyeDetailIntensity;

const float theta = 0.1;
layout(location = 0) out vec4 FragColor;

void main()
{
    //firstly, smooth
    vec4 preColor = texture(blurImageTex, textureCoord);
    
    vec4 inColor = texture(srcImageTex, textureCoord);
    vec3 meanColor = preColor.rgb;

    
    float p = clamp((min(inColor.r, meanColor.r-0.1)-0.2)*4.0, 0.0, 1.0);
    float kMin = (1.0 - preColor.a / (preColor.a + theta)) * p * blurAlpha;
    
    float maskValue = defaultMaskValue;     // 50% intensity
    if (useMask == 1) {
        vec3 mask_rgb = texture(beautyMaskTexture, maskTexCoord).rgb;
        float threshold = 0.005;
        if (mask_rgb.r > threshold && mask_rgb.b <= threshold) {
            maskValue = mask_rgb.r;
        } else if (mask_rgb.r > threshold && mask_rgb.b > threshold) {
            maskValue = 1.0 - mask_rgb.b;
        }
    }
    
    vec3 smoothColor = mix(inColor.rgb, meanColor.rgb, kMin * maskValue);


    //secondly, sharpen
    float sum = texture(srcImageTex,textureShift_1).g;
    sum += texture(srcImageTex,textureShift_2).g;
    sum += texture(srcImageTex,textureShift_3).g;
    sum += texture(srcImageTex,textureShift_4).g;
    sum = sum * 0.25;
    
    float hPass = inColor.g - sum + 0.5;
    float flag = step(0.5, hPass);
    
    vec3 tmpColor = vec3(2.0 * hPass + smoothColor - 1.0);
    vec3 sharpColor = mix(max(vec3(0.0), tmpColor), min(vec3(1.0), tmpColor), flag);
    
    vec3 epmColor = mix(smoothColor.rgb, sharpColor, sharpen);
    
    
    // thirdly, 
    if (eyeDetailIntensity >= 0.01) {

        vec3 eyeDetailMask = texture(eyeMaskTexture, maskTexCoord).rgb;
        
        if(eyeDetailMask.b > 0.005 && eyeDetailMask.r < 0.005 ) {
            vec3 sumColor = clamp(meanColor + (smoothColor.rgb - meanColor) * 2.5, 0.0, 0.6);
            sumColor = max(epmColor, sumColor);
            epmColor = mix(epmColor, sumColor, eyeDetailIntensity * eyeDetailMask.b * 0.55);
        }
    }

    // FragColor = vec4(epmColor, 1.0);
    FragColor = texture(srcImageTex, textureCoord);
}