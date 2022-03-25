#version 330 core 


in vec3 attPosition;
in vec2 attUV;
out vec2 textureCoordinate;

void main()
{
    gl_Position = vec4(attPosition, 1.);
    
    //textureCoordinate = attUV;
    
     textureCoordinate = clamp(attUV, 0.0, 1.0);
    //textureCoordinate = vec2(attPosition.xy/2+0.5);
}
