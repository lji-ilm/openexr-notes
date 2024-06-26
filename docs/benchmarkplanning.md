# Investigate compression rate first

The profiling of compression speed/IO performance part might need more technical effort and is hardware dependent.

Meanwhile the compression rate evaluation is static (only look at file/bytestream sizes) and could be operated from python.

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
However, since we do not deal with color science here, students should have an easy way to just "see the pictures" regardless if color display is accurate or not.

These software could be used cross platform:

1. GIMP - tried and verified. Not the most up to date EXR code but it always display something for you to look at.
2. mrv2 - small and nimble, but is professional grad image viewer https://mrv2.sourceforge.io/
3. openRV - student need to build from source, but more comphrensive. https://github.com/AcademySoftwareFoundation/OpenRV/tree/main

Not sure about imagemagick, maybe not Windows friendly.

# Rendering more synthetic test data

First of all, we should organize a batch of singal-processing oriented synthetic data. 
The open source repo has a few checker boards, but we might want more (different frequency domain feature, row v.s. column directional frequency, color channel differences, etc)

For example considering those standard DIP/Computer Vision datasets: https://www.imageprocessingplace.com/root_files_V3/image_databases.htm
Their dynamic range is insufficient to test EXR's capability, but we might pull a few from there if we have a HDR source (ex. astronomy pseudo color photos - if we have the source data and view transformation, then we can transform them again into HDR photos.)

For rendering:

Blender supports EXR since blender 4. Look at cycles demo scenes https://www.blender.org/download/demo-files/#cycles.
Check license.

Look at AnimalLogic's Alab Project: https://animallogic.com/alab/

Look at pbrt's scene repo which is academic friendly: https://github.com/mmp/pbrt-v4-scenes

pbrt directly renders into EXR: https://pbrt.org/users-guide-v4

Need ILM support to get more renderable sets.

Standard graphics assets like Conell Box and Standford bunny should be included. These could server as introductory exercise of how to use blender and output into exr, and we will have better control of the property of the resultant exr bytestream (ex. singal range, frequency, etc)


