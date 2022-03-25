#version 330 core 
in vec2 attPosition;
in vec2 attUV;
in float attOpacity;


out vec2 texCoord;
out vec2 maskTexCoord;


void main(){
    //gl_Position = vec4(attPosition.x*2-1,(1-attPosition.y)*2-1, 0.0, 1.0);
    gl_Position = vec4(attPosition.xy, 0.0, 1.0);
    texCoord = 0.5 * gl_Position.xy + 0.5;
    vec4 coord = vec4(attUV.x,1-attUV.y, 0.0, 1.0);
    maskTexCoord = coord.xy;
}
