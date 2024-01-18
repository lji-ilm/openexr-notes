## Notes on compression half of scene-linear data

The runtime (in-RAM) design of EXR focuses on organizing half into images (stratified 2D grids), but there isn't much thought into designing a persistent storage format, except for a few compressors available in the EXR library to reduce the size of a raw half stream.
Designing a good persistent storage format that maps into a runtime format is a large topic, a few example issues are named below, but there are many more:

1. Compression - We will only discuss this aspect in this note.
2. Progressive encoding - important for displaying a lossy image quickly using only the first parts of an image's bytestream. This can be implemented as a fast video player on an EXR stack and only starts to decode a lossless image when the video is paused. See: https://www.hostinger.com/tutorials/website/improving-website-performance-using-progressive-jpeg-images
3. Transmission loss resiliency - import for transmitting large chunks of data over the network, and effectively recovering maximum amount of data even when the transmission isn't consistent. See example: http://wind.lcs.mit.edu/papers/pv2002.pdf

We will only consider **compression** in detail here.

The opportunities to improve openEXR's compression beyond current deflate-class tools are mostly around two distinct features of openEXR.
As a starting point, remember that deflate-class tools (zip, gzip, zlib etc) do not make any assumptions about the byte stream being compressed. 
It treats the input as a byte buffer with perfectly randomized bytes and try to compress it as far as it can.

However, in OpenEXR's byte stream, two important pieces of pre-knowledge can be exploited to improve compression on top of deflate's general method:

1. The `half` floating point format is organized in an image (a stratified 2D regular grid).
2. The fact that it encodes scene-linear data before display mapping. 
I had some debate myself about what this "scene-linear" or "scene-referenced" _RGB_ actually means, but speaking in a vague and practical way, these numbers are closer to radiometry samples of visible lights than to pixel values (LED display voltage) for your screen.

These two, when considered together, lead to a few points about compression that worth considering:

1. First, a compression method that specializes in floating point data, such as zfp https://computing.llnl.gov/projects/zfp ([paper](../resources/PLindstorm_Integer.pdf) would probably perform better than deflate. 
zfp only works on IEEE 32 bits float, but adopting that for `half` should actually end up with a simpler algorithm.

2. Second, because the numbers in EXR is similar to a radiometry scan, the result stream of `half` numbers, both in tile format and in scanline format, should exhibit properties similar to a radiometry signal too. 

The most obvious property is the locality and frequency distribution of this signal. 
As with most continuous physical sampling of the real world, as long as the resolution is high enough, the signal should be mostly low frequency "smooth" with few high frequency "jumps" around boundaries. 
These boundaries can be either geometric (as across object boundaries) or rendering parametric (as across a specular spot on an object's surface). 
The openEXR team empirically noted this by the observation that the exponent byte varies slower than the mantissa byte, and wrote a byte swizzle in the internal zip implementation to compress the exponent byte separately from the mantissa byte. 
This implementation does introduce a performance penalty, however, as the bytes must be swizzled back upon decompression. 

This property can be exploited further. As early as in a piece of [JPEG2000 work](../resources/MGamito_JPEG2000.pdf), people have noticed that separately compress sign, exponent and mantissa lead to better results for floating point image data. 

More sophisticated methods were examined in a [paper](../resources/MIsenburg_floatingpointGeometry.pdf) also by Peter Lindstorm (Peter is the initial author of zfp, when it was still a research project).
This particular paper concerns compressing a geometry stream represented in IEEE floats; that is, the numbers are the XYZ coordinates of vertices of a mesh.
In this geometry stream (axis separated - X/Y/Z are 3 float streams), similar localities can be exploited if the vertices are somewhat sorted. 
It is easy to see that if a part of a large mesh has all its vertices placed together in the stream, then this part of the stream would also have a slowly varying exponent and a rapidly varying mantissa, because all vertices of this part would be bounded by the spatial extent of this mesh part.
The research then proceeds to compress exponent and mantissa separately and use them to predict each other.
However Peter himself later acknowledged that this inter-dependent predictor design is too complicated and favored the simpler method introduced in zfp.