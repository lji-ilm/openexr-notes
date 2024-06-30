# Benchmark of benchmark for EXR
This exercise's goal is to test water how difficult it is to benchmark and profile EXR at scale.
And gather ancedotal/practical technical experiences. 

The exercise invloves:
1. Total 3 EXR files as "testing of test" materials.
2. Compiling the C++ and C interface.
3. Load the 3 EXR demo files and compress into different formats at the current repo tip. Measure compression ratio.
4. Try profiling the running speed of the compression/decompression but not targeting statistical evidence.

The exercise will not involve:
1. Extensive amount of data (many different pictures etc)
2. Different file formats for the same image content, scanline vs tile etc. We do not test that in this stage. We only use 3 image files for testing and that's the full scope of this exercise.
3. Statistical profiling. Instead we only aim at single shot profiling data of limited number of runs of compression/decompression.

## Materials

3 Pictures.

1. Openexr-images: recommend for desk.jpg, can download.
2. ACES-testimages: recommend for sonyf35stilllife, downloaded.
3. HDR Photograhic survey: recommend for goldengate2 http://markfairchild.org/HDRPS/Scenes/GoldenGate(2).html
