#version 330 core 
in vec3 attPosition;
in vec2 attUV;

uniform float texBlurWidthOffset;
uniform float texBlurHeightOffset;

out vec2 textureCoord;
out vec4 texBlurShift1;
out vec4 texBlurShift2;
out vec4 texBlurShift3;
out vec4 texBlurShift4;

void main()
{
    gl_Position = vec4(attPosition, 1.0);
    textureCoord = attUV;
    
    vec2 singleStepOffset = 1.5*vec2(texBlurWidthOffset, texBlurHeightOffset);
    
    texBlurShift1 = vec4(attUV - singleStepOffset, attUV + singleStepOffset);
    texBlurShift2 = vec4(attUV - 2.0*singleStepOffset, attUV + 2.0*singleStepOffset);
    texBlurShift3 = vec4(attUV - 3.0*singleStepOffset, attUV + 3.0*singleStepOffset);
    texBlurShift4 = vec4(attUV - 4.0*singleStepOffset, attUV + 4.0*singleStepOffset);
}