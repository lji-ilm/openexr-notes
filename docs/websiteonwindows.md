# How to build website on Windows

1. Checkout your fork into a local dir, preferrably not inside Documents because Windows security policies. Github desktop can be used.
2. Install python (official download) into another folder, use the installer version (has pip).
3. Pip install `sphinx`, `breathe`, `sphinx-press-theme`. These are the only requirements when one ignores building the C API.
4. the bin is `Scripts\sphinx-build`, the command is `sphinx-build -b html <openexr>\website <build dir>

Example:
1. clone exr into `c:\ASWF\openexr\`
2. install python and pip all requirement into `c:\ASFW\python312`
3. create sphinx output dir `mkdir c:\ASWF\sphinx`
4. call `c:\ASWF\python312\Scripts\sphinx-build -b html c:\ASWF\openexr\website\ c:\ASWF\sphinx`
5. use a browser to view `c:\ASWF\sphinx\index.html`

One can go from there, change website and view results, and use Github desktop to manage the workflow.
