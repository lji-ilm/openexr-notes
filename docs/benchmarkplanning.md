# Investigate compression rate first

The profiling of compression speed/IO performance part might need more technical effort and is hardware dependent.
Meanwhile the compression rate evaluation is static (only look at file/bytestream sizes) and could be operated from python, if the python binding become functional by the time the students join. 

# Test data source - HDR Photographic survey 

Each picture can be downloaded separately on the website, comes with a compositing Mosaic and some metadata.
The fundamental property of this dataset is that it is all photographic.

Example - 1st picture: 

http://markfairchild.org/HDR.html
http://markfairchild.org/HDRPS/Scenes/PeckLake.html

# Test data source - ACES EXR 1.6 benchmark dataset

https://github.com/ampas/aces-dev/tree/dev/images

The problem of this dataset is that essentially it only have 3 distinct contents.
In other words, we'll only be interested in the 3 original pictures, quoting the above website:

- camera/
- DigitalLAD.2048x1556.dpx - original file representative of a film scan
- SonyF35.StillLife.dpx - pictorial camera original file
- syntheticChart.01.exr - a synthetic test chart

All other files on this repo are color space transformations in ACES applied to the 3 original images, which we might not care as much.
They could be used in some tests, as numbers in the raw EXR bytestream would be different; but if we have a better option we should not be using all these.

# Viewing EXR images - for sanity check purposes

EXR stores scene linear RGB and in theory need a view transform until it is viewable.
However, since we do not deal with color science here, students should have an easy way to just see the pictures.

These software could be used cross platform:

1. GIMP - tried and verified. Not the most up to date EXR code but it always display something for you to look at.
2. mrv2 - small and nimble, but is professional grad image viewer https://mrv2.sourceforge.io/
3. openRV - student need to build from source, but more comphrensive.

# Rendering more synthetic test data

Blender supports EXR since blender 4. Look at cycles demo scenes https://www.blender.org/download/demo-files/#cycles.
Check license.

Look at AnimalLogic's Alab Project: https://animallogic.com/alab/

Look at pbrt's scene repo which is academic friendly: https://github.com/mmp/pbrt-v4-scenes

Need ILM support to get more renderable sets.

Standard graphics assets like Conell Box and Standford bunny should be included. These could server as introductory exercise of how to use blender and output into exr, and we will have better control of the property of the resultant exr bytestream (ex. singal range, frequency, etc)


