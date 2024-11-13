// Need to set LD_LIBRARY_PATH to openimageio's dist folder (at runtime. compile/link time path has been written in makefile)
// export LD_LIBRARY_PATH=/home/lucky/ASWF/oiio/OpenImageIO/dist/lib
#include <OpenImageIO/imageio.h>
#include <chrono>

using namespace OIIO;
using std::chrono::steady_clock;

void simple_read(char * filename)
{
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

double
timing(steady_clock::time_point start, steady_clock::time_point end)
{
    return std::chrono::duration<double>(end - start).count();
}

// The GIMP case - read scanline one by one 
void 
read_scanline_sequentially_one_by_one(const char * filename)
{
    auto inp = ImageInput::open(filename);
    if (! inp) {
        std::cout << "OIIO cannot open the input test file." << std::endl;
        std::cout << filename << std::endl;
        return;
    } else
    {
        std::cout << "OIIO Opened this file: " << filename << std::endl;
    }

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
    std::cout << "nchannles:" << nchannels << std::endl;

    int tileWidth = spec.tile_width;
    std::cout << "tileWidth:" << tileWidth << std::endl;

    auto pixelType = TypeDesc::FLOAT;
    int bpc = 4;
    int bpp = bpc * nchannels;

    if (tileWidth == 0) {
        auto pixel_row = std::unique_ptr<unsigned char[]>(new unsigned char[xres * bpp]);
        // == Timing
        steady_clock::time_point startRead = steady_clock::now();
        for (int y = 0; y < yres; ++ y)
        {
            inp->read_scanline(y, 0, pixelType, &pixel_row[0]);
        }
        steady_clock::time_point endRead = steady_clock::now();
        // == Timing
        std::cout << " Read time : " << timing(startRead, endRead) << std::endl;
    }
    else
    {
        std::cout << "This is a tiled image so did not do the per-scanline experiment. (can be included in Case: Format Mismatch)" << std::endl;
    }

}

int main()
{
    const char* filename = "/home/lucky/ASWF/testimages/test_haaninjo.exr";
    //simple_read(filename);
    read_scanline_sequentially_one_by_one(filename);
    return 0;
}