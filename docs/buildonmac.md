# Build OpenEXR with the new python binding on a Mac

This note is a futher explaination based on the installation page (https://openexr.com/en/latest/install.html#install) about how to build the openexr repo with the new python binding on Mac (Apple silicon), and import the locally built python binding in a python environment.

The note is divided into two steps. In the first step we attempt to build the openEXR and the new python binaries, resulting in the `OpenEXR.so` importable to python. The second part discuss how to use this in python.

## Build EXR repo with homebrew

First, we need homebrew. Follow the official instruction to get homebrew on your mac if you haven't done so.

https://brew.sh/

One should follow through the tutorial and add `brew` to your shell environment so to call it easily. This following command assumes one uses `zsh`.

```
> (echo; echo 'eval "$(/opt/homebrew/bin/brew shellenv)"') >> /Users/${USER}/.zprofile
```

We need git and cmake. For most other ASWF projects too.

```
> brew install git cmake
> git --version
> cmake –version
```

Then, clone the official repo. In the current repo tip, it does not build the new python binding by default, so we need to turn on that option to allow the python binding getting built. Maybe in the future, building python binding will be turned on as default, so we don't need to change the cmake file anymore.

```
git clone https://github.com/AcademySoftwareFoundation/openexr.git
```

Find this line in your local clone and change it to ON:

https://github.com/AcademySoftwareFoundation/openexr/blob/b2d815602eeca1e31505650cd4acaf21bd9b2d87/cmake/OpenEXRSetup.cmake#L66

The python binding has a dependecy of `pybind11`. You need to install this depedency before you can build the OpenEXR bindary and its python bindings.

https://formulae.brew.sh/formula/pybind11

Then we can follow the official instructions about how to build OpenEXR. Note that we want to remove the cmake install instructions, since with python, we are likely to use the binding in a virtual environment, instead of install it into the MacOS system.

The following is copied from the official build instruction but with install removed. Refer to https://openexr.com/en/latest/install.html#build-from-source for more details.


```
% cd $builddir
% cmake $srcdir 
% cmake --build $builddir --config Release
```

I hope everything builds with these. To check if the python binding binary is successfully generated, go to `$builddir/src/wrappers/python` and check if the file named `OpenEXR.so` is there.

## Use the built binding in a python venv

It is in general a good practise to separate development projects in python by using virtual environments (venv) instead of install everything into the OS's python dist folder. We'll set up a venv to use the newly built openEXR binding.

First, get `python` on your mac if you haven't done so. It is typically sufficient to run `brew install python`, but the official site https://docs.brew.sh/Homebrew-and-Python gives more detailed instructions.

Next, create a virtual environment somewhere in your user space using the python you just installed. https://docs.python.org/3/library/venv.html

Go to this venv, activate it, and install `numpy` into this venv by using pip. Note, the binding requires numpy to run, but it is only a runtime requirement, not a build time requirement (build time only requires pybind11).

**DO NOT** `pip install OpenEXR` as this will install the old binding written by someone else, and create naming conflicts for the new binding binary we just built.

Lastly, navigate to the folder where you have the previously built `OpenEXR.so`. Launch python (the venv python!) here, and try `import OpenEXR`. This is a quick way of validating if the built binding is importable without properly set `PYTHON_PATH`. 

## Use the built binding in Jupyter notebook

It's also best if the jupyter server is installed in a venv, instead of directly in the OS's dist folder. If this is already done, one can simply copy the `OpenEXR.so` into this venv's `site_packages` folder and it becomes importable in the notebooks. As above, one needs numpy too.


