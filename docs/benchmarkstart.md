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

## Additional Benchmarking data:

1. Cornell Box team has photogrametrically accurate pictures of the real box: https://www.graphics.cornell.edu/online/box/data.html. These are single wavelength measurements, and a spectural responsibility curve of RGB is required to integrate them into the RGB picture. 
2. Stanford bunny's lab maintains a bunch of 3d models one can use for research. https://graphics.stanford.edu/data/3Dscanrep/ One might figure out how to render these with Blender 4.
3. Note that Blender 4 will release a LTS on the version 4 line soon.
4. Blender supports saving to EXR and EXR multi-channel since 2015. Investigate which version of OpenEXR they use in Blender 4

## Kimball's performance.cpp
Kimball wrote a simple profiler under `src/test/OpenEXRCoreTest`.
Here: https://github.com/AcademySoftwareFoundation/openexr/blob/main/src/test/OpenEXRCoreTest/performance.cpp

This little code compiles into its own binary called `bin/CorePerfTest` upon a full build. 
It seems the data it outputs mainly concerns the "advantage" of the Core implementation over the Imf C++ implementation. 
Running it over the 3 test images i've got yields the following results, and there are some small problems when running (there is an ERROR about "different pixel counts" and ilmimf read exactly 0 pixels).

It might be worthwhile to take this as my starting point to write a better profiling tools, while let the students to repeat the run on datasets.

```
/mnt/c/ASWF/openexr/build/bin$ ./CorePerfTest ../../../testimages/ACES.StillLife.exr
ERROR: different pixel counts recorded: core 41472000 ilmimf 0
Stats for reading: 1 files 20 times

 Timers  Core            IlmImf
 Header: 31789863        38346265        ns
   Data: 2063014509      5770097652      ns
  Close: 7213395         7350797         ns
  Total: 2102017767      5815794714      ns

 Ave     Core            IlmImf
 Header: 1.58949e+06     1.91731e+06     ns
   Data: 1.03151e+08     2.88505e+08     ns
  Close: 360670          367540          ns
  Total: 1.05101e+08     2.9079e+08      ns

 Ratios
 Header: 1.20624
   Data: 2.79693
  Close: 1.01905
  Total: 2.76677
/mnt/c/ASWF/openexr/build/bin$ ./CorePerfTest ../../../testimages/OpenEXR.Desk.exr
ERROR: different pixel counts recorded: core 11540480 ilmimf 0
Stats for reading: 1 files 20 times

 Timers  Core            IlmImf
 Header: 40235703        58463903        ns
   Data: 345774415       534539126       ns
  Close: 11938501        10699600        ns
  Total: 397948619       603702629       ns

 Ave     Core            IlmImf
 Header: 2.01179e+06     2.9232e+06      ns
   Data: 1.72887e+07     2.6727e+07      ns
  Close: 596925          534980          ns
  Total: 1.98974e+07     3.01851e+07     ns

 Ratios
 Header: 1.45304
   Data: 1.54592
  Close: 0.896226
  Total: 1.51704
/mnt/c/ASWF/openexr/build/bin$ ./CorePerfTest ../../../testimages/HDRSurvey_GoldenGate.exr
ERROR: different pixel counts recorded: core 244244480 ilmimf 0
Stats for reading: 1 files 20 times

 Timers  Core            IlmImf
 Header: 43784521        48037118        ns
   Data: 4389283827      6516039266      ns
  Close: 8872803         78286440        ns
  Total: 4441941151      6642362824      ns

 Ave     Core            IlmImf
 Header: 2.18923e+06     2.40186e+06     ns
   Data: 2.19464e+08     3.25802e+08     ns
  Close: 443640          3.91432e+06     ns
  Total: 2.22097e+08     3.32118e+08     ns

 Ratios
 Header: 1.09713
   Data: 1.48453
  Close: 8.82319
  Total: 1.49537
```
