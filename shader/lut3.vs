#version 330 core 

in vec3 attPosition;
in vec2 attUV;
out vec2 textureCoordinate;
void main(void) {
    gl_Position = vec4(attPosition, 1.);
    textureCoordinate = attUV;
}
