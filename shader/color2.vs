#version 330 core 
in vec3 attPosition;
in vec2 attUV;

out vec2 textureCoord;
out vec2 maskTexCoord;

uniform float widthOffset;
uniform float heightOffset;

out vec2 textureShift_1;
out vec2 textureShift_2;
out vec2 textureShift_3;
out vec2 textureShift_4;

void main()
{
    gl_Position = vec4(attPosition, 1.0);
    //attUV = vec2(attUV.x,1-attUV.y);
    textureCoord = vec2(attPosition.xy/2+0.5);
    maskTexCoord = vec2(attUV.x,1-attUV.y);
    

    textureShift_1 = vec2(textureCoord + 0.5 * vec2(widthOffset,heightOffset));
    textureShift_2 = vec2(textureCoord + 0.5 * vec2(-widthOffset,-heightOffset));
    textureShift_3 = vec2(textureCoord + 0.5 * vec2(-widthOffset,heightOffset));
    textureShift_4 = vec2(textureCoord + 0.5 * vec2(widthOffset,-heightOffset));
}
