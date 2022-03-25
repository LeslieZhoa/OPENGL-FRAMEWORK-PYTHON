#version 330 core 
in vec3 attPosition;
in vec2 attUV;
out vec2 texCoordinate;

void main() {
    gl_Position = vec4(attPosition, 1.0);
    texCoordinate = attUV;
}
