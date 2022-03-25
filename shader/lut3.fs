#version 330 core 

uniform sampler2D inputImageTexture1;
uniform sampler2D inputImageTexture2;
uniform sampler2D inputImageTexture3;
in vec2 textureCoordinate;
uniform float leftIntensity;
uniform float rightIntensity;
uniform float mposition;

layout(location = 0) out vec4 FragColor;
void main()
{
    vec4 textureColor1 = texture(inputImageTexture1, textureCoordinate);
    textureColor1 = clamp(textureColor1, 0.0, 1.0);
    
    float blueColor = textureColor1.b * 63.0;
    
    vec2 quad1;
    quad1.y = floor(floor(blueColor) / 8.0);
    quad1.x = floor(blueColor) - (quad1.y * 8.0);
    vec2 quad2;
    quad2.y = floor(ceil(blueColor) / 8.0);
    quad2.x = ceil(blueColor) - (quad2.y * 8.0);
    
    vec2 texPos1;
    texPos1.x = (quad1.x * 0.125) + 0.5/512.0 + ((0.125 - 1.0/512.0) * textureColor1.r);
    texPos1.y = (quad1.y * 0.125) + 0.5/512.0 + ((0.125 - 1.0/512.0) * textureColor1.g);
    vec2 texPos2;
    texPos2.x = (quad2.x * 0.125) + 0.5/512.0 + ((0.125 - 1.0/512.0) * textureColor1.r);
    texPos2.y = (quad2.y * 0.125) + 0.5/512.0 + ((0.125 - 1.0/512.0) * textureColor1.g);
    
    if(textureCoordinate.x<mposition){
        FragColor = vec4(1.0);
        vec4 newColor2_1 = texture(inputImageTexture2, texPos1);
        vec4 newColor2_2 = texture(inputImageTexture2, texPos2);
        vec4 newColor22 = mix(newColor2_1, newColor2_2, fract(blueColor));
        FragColor = mix(textureColor1, vec4(newColor22.rgb, textureColor1.w), leftIntensity);
    }else{
        vec4 newColor3_1 = texture(inputImageTexture3, texPos1);
        vec4 newColor3_2 = texture(inputImageTexture3, texPos2);
        vec4 newColor33 = mix(newColor3_1, newColor3_2, fract(blueColor));
        FragColor = mix(textureColor1, vec4(newColor33.rgb, textureColor1.w), rightIntensity);
    }
}
