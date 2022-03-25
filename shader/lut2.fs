#version 330 core 

in vec2 texCoordinate;

uniform sampler2D inputTex;

uniform sampler2D lutImageForClear;
uniform float clearIntensity;

layout(location = 0) out vec4 FragColor;

vec4 LUT8x8(vec4 inColor, sampler2D lutImageTexture)
{
    float blueColor = inColor.b * 63.0;
    
    vec2 quad1;
    quad1.y = floor(floor(blueColor) / 8.0);
    quad1.x = floor(blueColor) - (quad1.y * 8.0);
    vec2 quad2;
    quad2.y = floor(ceil(blueColor) / 8.0);
    quad2.x = ceil(blueColor) - (quad2.y * 8.0);
    
    vec2 texPos1;
    texPos1.x = (quad1.x * 0.125) + 0.5/512.0 + ((0.125 - 1.0/512.0) * inColor.r);
    texPos1.y = (quad1.y * 0.125) + 0.5/512.0 + ((0.125 - 1.0/512.0) * inColor.g);
    vec2 texPos2;
    texPos2.x = (quad2.x * 0.125) + 0.5/512.0 + ((0.125 - 1.0/512.0) * inColor.r);
    texPos2.y = (quad2.y * 0.125) + 0.5/512.0 + ((0.125 - 1.0/512.0) * inColor.g);
    
    vec4 newColor2_1 = texture(lutImageTexture, texPos1);
    vec4 newColor2_2 = texture(lutImageTexture, texPos2);

    vec4 newColor22 = mix(newColor2_1, newColor2_2, fract(blueColor));

    return newColor22;
}

void main() {
    vec4 inColor = texture(inputTex, texCoordinate);
    vec4 dstColor = inColor;

    // first clear (z-order 1200)
    // if (clearIntensity > 0.0) {
    //     vec4 clearColor = LUT8x8(dstColor, lutImageForClear);
    //     dstColor = mix(dstColor, clearColor, clearIntensity);
    // }


    FragColor = dstColor;
}

