# What are the common technical access patterns to images in VFX/Animation industries?

## Introduction
We are investigating how images are used in the media industries to better inform development of fundamental softwares in ASWF, such as OpenImageIO and OpenEXR, amongst others.

This is a *technical* investigation related how end-user software interact with data formats and software library for image files. It is not about creative workflows around the content of visual images, such as compositing or color grading.

For example, one such way of "interact" might be an image editor, such as GIMP, reading one scanline at a time from an OpenEXR file. Another way of "interact" might be a rendering enging reading a few tiles in a MIPMAP texture in order to compute surface shading of a 3D mesh. 

In the following sections we define access patterns, report previous research and open the floor to discussion.

## Access Pattern for Image Reads

An end-user software package can read and write data into an image file. 
To restrict the scope of our first stage investigation, here we only concern with reading data from an image file. 

When reading an image, an end-user software package might do various different things. For example, it might not need the whole image so it only read a part of the file on the disk. It might only need certain color channels, so it ignores the other color channels and data (such as alpha and transparency). It might read in big or small chunks to get the data from the file on disk. It might read a part first and another part next. These are the access **behaviours**. 

One software package typically have many different behaviours when it read images, dependes on the workflow context, the image format, and other environments. However, for a specific production context and use cases, sometimes we can find access **patterns** from a large set of various behaviours. These patterns are what we are interested to discover because they can be mapped onto **optimization goals** of the fundamental digital image libraries in ASWF. 

For a simple example, if a studio keeps using an end-user software package in a specific creative workflow, and we somehow knows that the workflow access the image in scanlines, then we can try to deeply optimize scanline access in ASWF libraries. These targeted optimizations, in turn, will likely introduce a tangible benefit for the studio's operations.

The access patterns may emerge from the total possibility of all access behaviours related to the following factors:

1. The end-user software package being used. Certain software prefers to access images in specific ways because it's best for what they're designed for.
2. The creative workflow and the production context. 3D computer animation and traditional hand-drawn 2D animation are likely to access images in production following different pattens. A VFX studio that deals with a large amount of camera on-set images is likely to have a different access pattern compared to an Animation studio where all frames are synthetic from rendering.
3. The user habit. An artist or a group of artists may prefer to use software tools in a different way compared to other goups, resulting in the software tool accessing images differently.

We can discover these access patterns in many ways, including:

1. Anecdotally. By asking studio experts and software vendors to report by experiences what are the most likely patterns. This is what we're trying to do here.
2. By Instrumentation. We can insert statistics to the fundamental digital image software libraries and distribute these instrumented libraries to studios. By using these libraries in real-world production, the statistics collected would reveal the ground-truth access pattern of images. This methodology is considered a future stage of our investigation.

## Preivous Work