# Build OIIO with specific openEXR commits

OIIO can be built against any EXR builds, but the difficulty in running this on linux is to ensure that OIIO's building and linking does not pick up a default EXR dist in the system. In this exercise we can use any OIIO versions, typically the latest release would be okay.

If we have two EXR builds whose ABIs are the same, OIIO will use them as run-time dynamic link libraries and a direct `.so` swap can work. 
But as far as I know EXR typically changes ABI on a minor release, and sometimes even so on a bug fix release.
So this note is mostly concerning to actually **re-build** OIIO aganist a specific commit, and how to reset the building environment so OIIO can be built aganist the next specific commit.

---

First, clone the standard OIIO repo and attempt to configure `cmake` by simply

```
cd <oiio-clone-dir>
mkdir build
cd build
cmake ..
```

OIIO's `cmake` configuration files will attempt to search for dependencies. It is best if this process is started on a clean VM/WSL/Linux install, such that it is guaranteed IMath and OpenEXR are not in the system. 

Observe the `cmake` depedency checking output, and install any packages that we do **not** want to interrogate directly into the system area. This typically means JPEG, turbo-JPEG, PNG and TIFF. Stop at a point when the cmake dependecy checker says it cannot find IMath, and suggest you to set the Imath_ROOT varaible. If this never happened, it means you already have a copy of Imath (and probably also openEXR) in your system and it's best to reset the whole system/vm and start over.

---

Now, use Larry's build script to build openexr by calling https://github.com/AcademySoftwareFoundation/OpenImageIO/blob/main/src/build-scripts/build_openexr.bash 

Note how the build and dist dir are construed in the building script. It all starts with a `pwd`, e.g. current working directory, so where this script getting called is important.

The script accepts an environment variable `OPENEXR_VERSION`. This can be a version string `vx.x.x` or just a commit string. This variable should be exported before calling this script.

At the end of this script, the script will automatically export `OpenEXR_ROOT`. If you continue to cmake oiio in the same shell this is good to use. If you are opearting oiio build in another shell, note this path and export both `Imath_Root` and `OpenEXR_ROOT` in the other shell.

---

Now return to the context of the first step. Export the Imath_ROOT first, and run cmake configure again. Observe that the Imath dependecy has been found, and OpenEXR is missing. Then export OpenEXR_ROOT and cmake configure again, making sure it is found. Proceed to actually build oiio with the `cmake --build ..` command.

---

To restart this process, first unset the `Imath_ROOT` and `OpenEXR_ROOT`, clean the oiio build, run cmake config again and making sure that cmake **cannot** find Imath and OpenEXR. 

Then Delete that `ext/dist` folder output by the build script. Rerun the build script and re link the root dirs to build Oiio again.

---

Since OIIO use dynamic link at runtime aganist `OpenEXR.so` on the LD path,even if the (testcase->OIIO->OpenEXR) chain is built correctly, it is still important that one checks for the correct version where the test runs in runtime linking. This is typically can be verified if the built test **cannot** start and report missing `.so` file if an extra `LDPATH` to the `ext/dist` folder where the specific EXR version was **not** set (this could typically be set in a terminal session so a new terminal will restart the experiment). Again to have a clean system that guarantees no system-wide openEXR is the key.  