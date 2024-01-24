EXR is supposed to store scene-linear, before display mapping, high-dynamic range RGB values. 
Although it still use RGB to represent a color, these RGB numbers in EXR are supposed to be not directly display-able.
They're more akin to radiometry numbers, where light intensity (such as lumen/m^2, or footcandles for the US...) are recorded.
This relates EXR to a physical measurements dataset, where an image (a 2D raster grid) of "numbers" of arbitrary range and meaning cannnot be trivially be displayed by treating them as pixel values on screen.

The discipline addressing the issue of "how to display a number dataset" is scientific visualization, and the specific topic regarding how to map an arbitrary numerical dataset's numbers to display calibrated RGBs is called **Transfer Function**.
A [seminal survey paper](../resources/starTransferFunction.pdf) a few years ago summerizes recent developments on this topic, although it's a bit overkill for EXR's purpose, since EXR is inherently 2D and biggest chanllenge in transfer function research is how to effectively mapping 3D (volumetic) numerical datasets.
For 2D images it typically boils down to color LUT tables or curves. 

## DICOM

[DICOM](https://en.wikipedia.org/wiki/DICOM) is a medical image format that turly intended to store images consists of none-visual numbers - the most common case being the number is the tissue absorbency of X-Ray on that pixel location.

DICOM is a wrapper container "format".
It does not specifiy how the image data itself is encoded inside the "datablocks" in the file; it merely provides mechanisms to keep metadata and specifies transfer protocols over the network.
Its "datablocks" can be any image format, for example jpeg or tiff.

There are infinite numbers LUT designs availables to DICOM data, some designs are tied to specific X-Ray or CT machines, others are tied to diagnostic scenarios (such as LUTs that emphasize the details in soft tissues over bones, or vice).
Of particular note is that the DICOM standard itself included a chapter called "DICOM grayscale standard display function (GSDF)", which takes a sample in a DICOM image and produce a displayable grey-scale value, in case if one is getting lost in the sea of 3rd party LUTs; or communication become a problem due to difference in LUTs.

## ImageJ

ImageJ, J2 and [Fiji](https://fiji.sc/) are powerhorse in scientific image processing used by the majority of the image processing community, particularly practioners (none-researchers, people work in commercial labs etc). 
There may be some merit to provide an openEXR reader to imageJ, since it is such a strong diagnostic tool (and with a great reputation).
Scientific community are well-known for its ability to (re)invent non-compatible image formats from every single lab, and ImageJ is (said) to be very easy to add an additional reader plugin.
