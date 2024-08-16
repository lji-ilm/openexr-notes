# openexr-wishlist

## A. Better compression

1. Better compression ratio - smaller persistent storage files. See notes.
2. Better performance in both compression and decompression. Particularly decompression (for playback).

    - See the recent [PR!1604](https://github.com/AcademySoftwareFoundation/openexr/pull/1604) for the blosc2+zstd.
    Note: This PR did many things, but blosc2 is primarily a **throughput performance optimization** library. zstd is the same fundamental algorithm as zlib/deflate, but the implementation is better.
    - For playback / preview speed, we may also consider _progressive encoding_, in addition to forcefully load the entire lossless image really fast...

## B. Curate a larger benchmark EXR dataset on the opensource repo.

Cary mentioned this. Currently, there are only about 20 real pictures as test images on the openexr repo, in addition to a few technical test pictures. 

This amount of test images would only be borderline sufficient for validation (e.g. does this work or not) but way too few for profiling (e.g. how fast/how much memory/how much network does this need).
Without a profiling benchmark, it's hard to say something (like a new compression) is good/performant/fast/small on disk, or not (we can only test if it is correct or not, with these limited samples).

Larry also mentioned in slack that performance was a pain-point for openEXR, compared to TIFF.

## C. Modify the website building script, removing the exr &rarr; jpeg conversion in website building to make it cross-platform.

One of the website building script, [test_images.py](https://github.com/AcademySoftwareFoundation/openexr/blob/e571107f1ee340bbb1b48e1a76f2e8c8f46d04c1/website/scripts/test_images.py) is a python3 script which downloads example images, convert them to jpeg, and dyanmically organize an `rst` file as the test-images page.

This script currently is written in a way that only works in Linux, as it dependes on `wget`, `which`, in addition to `convert` and `exrheader`.
It also dependes on linux path conventions instead of the Windows one. 
It is possible to make a robust, cross-platform test image conversion script, but it might be too much work as this is just for generating the example image page of the website.

In addition, I disucssed that the website should be self-contained editable. 
If a website editor (let's say it's not a very technical person) edited and previewed the website, but somehow the exr test image repo was updated, then the website will change appearance, and the editor would lose clue of why it changed after the edit.
Keep exr &rarr; jpg conversion outside the website building process will make the website editing more closely resemble a document editing workflow, and be more consistent/predicable for professional editors who are not tech savvy.

# Bibliography
https://developer.nvidia.com/gpugems/gpugems/part-iv-image-processing/chapter-26-openexr-image-file-format

Library of congress digital file format intelligence page:
https://www.loc.gov/preservation/digital/formats/fdd/fdd000583.shtml

Dreamworks contributed a lossy compression... what is that?
https://www.renderosity.com/article/17221/dreamworks-animation-contributes-lossy-compression-to-openexr-2-2

Mark Fairchild (mark.fairchild@rit.edu), a professor at RIT, did a benchmark dataset for HDR imaging research. This dataset is in EXR, probably in an earlier version. We should make use of it instead of starting from scratch.
http://markfairchild.org/HDR.html

#Start to do local scripting..

# Notes

- [Notes on floating point compression.](docs/compression.md)
- [Notes about Visualization](docs/visualization.md)
