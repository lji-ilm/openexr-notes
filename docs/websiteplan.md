# Plan for a PR for issue # 1580 Website 

## Goal 

1. Make sure website builds on Windows 10/11 natively
2. Use pre-compiled jpeg figures for website instead of download exr at website compile time and convert them into jpeg at website build time.
3. subsequently, remove test_image.py

## Plan

1. Understand how the CMAKE process and be able to replicate it by hand on Windows without using CMAKE
2. Understand where each pieces was used:
3. Doxgen? Which source code was run through?
4. Breath? where is breath temp dir?
5. Sphinx? Where is that template goes in on a sphinx windows native installation?
6. Where is test_image.py invoked and how to by pass it?
7. Can the step by step process be substituted by another job scheduler? powershell or plain python?
