#version 330 core 
in vec3 attPosition;     //vertex coordinate
in vec2 attUV;           //uv coordinate
in vec2 attStandardUV;   //uv coordinate of standard face

out vec2 maskTexCoord;


void main(){
    gl_Position = vec4(attPosition.x / * 2. - 1., 
                       attPosition.y / * 2. - 1., 
                       0.0, 
                       1.0);
    
    maskTexCoord = vec4(attStandardUV, 0., 1.)).xy;
}
