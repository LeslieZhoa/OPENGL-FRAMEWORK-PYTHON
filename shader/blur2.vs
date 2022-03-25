#version 330 core 
in vec2 attPosition;
in vec2 attUV;
uniform float texelWidthOffset;
uniform float texelHeightOffset;
out vec2 textureCoordinate;
out vec4 textureShift_1;
out vec4 textureShift_2;
uniform mat4 MVPMatrix;

void main(void)
{
    gl_Position = vec4(attPosition, 0., 1.);
    textureCoordinate = attUV;
    
    vec2 singleStepOffset = vec2(texelWidthOffset, texelHeightOffset);
    textureShift_1 = vec4(attUV - singleStepOffset, attUV + singleStepOffset);
    textureShift_2 = vec4(attUV - 2.0 * singleStepOffset, attUV + 2.0 * singleStepOffset);
}
