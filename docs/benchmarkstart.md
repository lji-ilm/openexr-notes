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

## Method

Exercise goals:

1. (Lvl 0) Practise open the 3-4 sample exrs with specialized software.
2. (Lvl 0) Practise forking and compiling openEXR repo, reading out metadata of the sample exrs.
3. (Lvl 0) Caculate the existing compression ratio, by calculating the raw size by hand and see the current compression ratio. 
4. (Lvl 1) Time the decompression time using process wrapper (one shot).
5. (Lvl 1) Load the raw buffer into the memory and write out a raw-exr file as benchmark checkpoint.
6. (Lvl 1) Load the raw buffer with all C++, C and python APIs, and time them.
7. (Lvl 2) Re-compression the raw buffer using different, built in compression method.
8. (Lvl 2) Re-compression with all C++, C and python APIs (can do?)
9. (Lvl 2) Time the raw-to-compression time using process warpper (one shot).
10. (Lvl 3) Time the decompression and raw-to compression using C++/C APIs (one shot), and recomplie the project with the instrumented code.

## What should I do myself on this?

1. Try to render a few heritage subject in EXRs, like cornell box/bunny. Blender 4 or Pbrt, prefer Blender 4.
2. Try to get Level 0-1-2 done myself with a compliation of openEXR Core C binary on Windows or WSL. Only do Core. One shoot benchmark.
