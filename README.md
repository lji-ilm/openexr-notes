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

# Notes

- [Notes on floating point compression.](docs/compression.md)
