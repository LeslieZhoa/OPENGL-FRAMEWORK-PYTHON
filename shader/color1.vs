#version 330 core 

in vec3 attPosition; // 移动后的坐标
//in vec2 attUV; // 移动前的坐标
in vec2 attStandardUV; // 标准坐标
out vec2 texUV;
out vec2 srcUV;

out vec4 textureShift_1;
out vec4 textureShift_2;
out vec4 textureShift_3;
out vec4 textureShift_4;

uniform float widthOffset;
uniform float heightOffset;

uniform int width;
uniform int height;

void main() {
    gl_Position = vec4(attPosition.x,attPosition.y, 0.2, 1.0);
   
    texUV = vec2(attStandardUV.x,1-attStandardUV.y);
    
    vec2 attUV = attPosition.xy/2+0.5;
    srcUV = vec2(attUV.xy);
    textureShift_1 = vec4(attUV + vec2(-widthOffset,0.0),attUV + vec2(widthOffset,0.0));
    textureShift_2 = vec4(attUV + vec2(0.0,-heightOffset),attUV + vec2(0.0,heightOffset));
    textureShift_3 = vec4(attUV + vec2(widthOffset,heightOffset),attUV + vec2(-widthOffset,-heightOffset));
    textureShift_4 = vec4(attUV + vec2(-widthOffset,heightOffset),attUV + vec2(widthOffset,-heightOffset));
}