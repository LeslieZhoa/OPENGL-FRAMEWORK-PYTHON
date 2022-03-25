#version 330 core 

in vec2 texCoord;
in vec2 maskTexCoord;
const float varOpacity=1.0;
const float varOpacityEyeDetail=1.0;
const float varOpacityPouch=1.0;
const float varOpacityNasolabialFolds=1.0;

uniform sampler2D inputImageTexture;
uniform sampler2D inputScaledTexture;
uniform sampler2D inputScaledBlurTexture;
uniform sampler2D inputImageMaskTexture;
uniform float intensity;
uniform float eyeDetailIntensity;
uniform float removePouchIntensity;
uniform float removeNasolabialFoldsIntensity;
layout(location = 0) out vec4 FragColor;

void main()
{
    vec4 color = texture(inputImageTexture, texCoord);
    vec4 maskColor = texture(inputImageMaskTexture, maskTexCoord);
    vec3 resultColor = color.rgb;

    // brighten eye
    if(maskColor.b > 0.005 && maskColor.r < 0.005 && eyeDetailIntensity >= 0.01)
    {
        vec2 step1 = vec2(0.00208, 0.0);
        vec2 step2 = vec2(0.0, 0.00134);
        vec3 sumColor = vec3(0.0, 0.0, 0.0);
        for(float t = -2.0; t < 2.5; t += 1.0)
        {
            for(float p = -2.0;p < 2.5; p += 1.0)
            {
                sumColor += texture(inputImageTexture,texCoord + t * step1 + p * step2).rgb;
            }
        }
        sumColor = sumColor * 0.04;
        sumColor = clamp(sumColor + (color.rgb - sumColor) * 3.0, 0.0, 1.0);
        sumColor = max(color.rgb, sumColor);
        resultColor = mix(color.rgb, sumColor, eyeDetailIntensity * varOpacityEyeDetail * maskColor.b * 0.5);
    }
    
    // remove eye pouch
    if(maskColor.r > 0.005 && maskColor.b < 0.005 && removePouchIntensity >= 0.01)
    {
        vec3 scaledColor = texture(inputScaledTexture, texCoord).rgb;
        vec3 scaledBlurColor = texture(inputScaledBlurTexture, texCoord).rgb;
        vec3 imDiff = clamp((scaledBlurColor - scaledColor) * 1.3 + 0.03 * scaledBlurColor, 0.0, 0.2);
        imDiff = min(resultColor+ imDiff, 1.0);
        resultColor = mix(resultColor, imDiff, removePouchIntensity * varOpacityPouch * maskColor.r);
    }
    
    // remove nasolabial folds
    if(maskColor.g > 0.005 && removeNasolabialFoldsIntensity >= 0.01)
    {
        vec3 scaledColor = texture(inputScaledTexture, texCoord).rgb;
        vec3 scaledBlurColor = texture(inputScaledBlurTexture, texCoord).rgb;
        vec3 imDiff = clamp((scaledBlurColor - scaledColor) * 1.4 + 0.05 * scaledBlurColor, 0.0, 0.3);//0.3
        imDiff = min(resultColor+ imDiff, 1.0);
        resultColor = mix(resultColor, imDiff, removeNasolabialFoldsIntensity * varOpacityNasolabialFolds * maskColor.g);
    }

    FragColor = vec4(mix(color.rgb, resultColor, intensity * varOpacity), 1.0);
}
