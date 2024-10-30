// Need to set LD_LIBRARY_PATH to openimageio's dist folder (at runtime. compile/link time path has been written in makefile)
// export LD_LIBRARY_PATH=/home/lucky/ASWF/oiio/OpenImageIO/dist/lib
#include <OpenImageIO/imageio.h>
using namespace OIIO;

void simple_read()
{
    const char* filename = "/home/lucky/ASWF/testimages/test_haaninjo.exr";

    auto inp = ImageInput::open(filename);
    if (! inp)
        return;
    const ImageSpec &spec = inp->spec();


    for (int i = 0;  i < spec.nchannels;  ++i)
    {
    std::cout << "Channel " << i << " is "
              << spec.channelnames[i] << std::endl;
    }

    int orientation = 0;
    bool ok = spec.getattribute("Orientation", TypeInt, &orientation);
    if (!ok) {
        std::cout << "No integer orientation in the file\n";
    } else
    {
        std::cout << "Orientation: " << orientation << std::endl;
    }

    float f = spec.get_float_attribute ("PixelAspectRatio", 1.0f);
    std::cout << "Pixel Aspect Ratio:" << f << std::endl;

    std::string s = spec.get_string_attribute ("ImageDescription", "");
    std::cout << "Image Description:" << s << std::endl;

    int xres = spec.width;
    int yres = spec.height;
    std::cout << "xres: " << xres << " yres: " << yres << std::endl;
    int nchannels = spec.nchannels;
    auto pixels = std::unique_ptr<unsigned char[]>(new unsigned char[xres * yres * nchannels]);
    inp->read_image(0, 0, 0, nchannels, TypeDesc::UINT8, &pixels[0]);
    inp->close();
}

int main()
{
    simple_read();
    return 0;
}