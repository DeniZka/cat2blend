# cat2blend
Imports Tamsoft models into blender

Testing on Senran Kagura Estival Versus models

Most parts was reversed by my self

Some parts was adviced by [Random Talking Bush](https://www.vg-resource.com/thread-29836.html). Thx bro, you saves bones tips

I'm using linux, so modify windows paths by your self. Sory win guys

#### whats works:
- cat file parser
- mesh parser (with bones)
- texture parser
- animations
#### whats in plan:
- armatures merging (when you customize your character)

#### how to use
1. open scripting tab
2. in any text windows select script choose "open_model_with.."
3. play this script
4. select any file with model or animation
    
#### how to load character poperly
- load some buras (texture only)
- load face
- load hair
- load body
    - select another body's texture skin_*** 

to load new body - remove textures and shaders

#### how to reset characher pose
sometimes some pose can overlap some another pose. Looks creepy
better way to reset pose
1. choose bones to reset
2. set pose mode
3. select all bones (A)
4. reset pose, rotation, scale (ALT+G, ALT+R, ALT+S)

![blender](doc/hello_blender.png)
![blender1](doc/hello_blender1.png)
![blender2](doc/hello_blender2.png)
