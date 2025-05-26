# How to build OIIO with a customized EXR version

This seems to change from time to time as both repo evolve. At the time of this note (May 2025) the eaisest way is this:

1. checkout OIIO and checkout the release branch/tag, unless you want to build OIIO on dev tip too.
2. Go to EXR repo and get into the view of whatever you want to build (on branch, on tag, or on a specific commit). Check the "current" version of this view in `src/lib/OpenEXRCore/openexr_version.h`. This will be the "version" of this openEXR build on this specific commit.
3. Now go back to the OIIO checkout, open file `src/cmake/build_OpenEXR.cmake`, edit the following two lines.

```
set_cache (OpenEXR_BUILD_VERSION $the_version_you_find$ "OpenEXR version for local builds")
set (OpenEXR_GIT_TAG $the_commit_or_branch_you_want_to_build$)
```

4. Now go back to the OIIO build folder, run the local dep build option. For example:

```
cmake .. -DOpenImageIO_BUILD_LOCAL_DEPS=all
```

This should get a local EXR built and get the generation step done. The next stage OIIO build may still have problems, but debug as we go!
