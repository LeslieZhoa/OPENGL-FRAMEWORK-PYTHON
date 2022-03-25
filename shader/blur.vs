#version 330 core 
layout(location = 0) in vec3 attPosition;
layout(location = 1) in vec2 attUV;

uniform float texelWidthOffset;
uniform float texelHeightOffset;
out vec2 textureCoordinate;
out vec4 textureShift_1;
out vec4 textureShift_2;
out vec4 textureShift_3;
out vec4 textureShift_4;

void main(void)
{
    gl_Position = vec4(attPosition, 1.0);
    textureCoordinate = gl_Position.xy; //attUV;
    textureCoordinate.x = (attPosition.x + 1) / 2;
    textureCoordinate.y = (1-attPosition.y) / 2;
    
    vec2 singleStepOffset = vec2(texelWidthOffset, texelHeightOffset);
    textureCoordinate = attUV;
    textureShift_1 = vec4(attUV - singleStepOffset, attUV + singleStepOffset);
    textureShift_2 = vec4(attUV - 2.0 * singleStepOffset, attUV + 2.0 * singleStepOffset);
    textureShift_3 = vec4(attUV - 3.0 * singleStepOffset, attUV + 3.0 * singleStepOffset);
    textureShift_4 = vec4(attUV - 4.0 * singleStepOffset, attUV + 4.0 * singleStepOffset);
}