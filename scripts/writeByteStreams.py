import os
import sys
from functools import cached_property

import numpy as np

class EXRByteStreams():
    def __init__(self, RGBData):
        assert(RGBData.dtype == np.half)
        shape = RGBData.shape()
        assert(shape[2] >= 3)
        
        self.width = shape[0]
        self.height = shape[1]
        self.num_pixels = width * height
        self.data = RGBData

    @cached_property
    def ROriginal():
        return self.data[:,:,0]

    @cached_property
    def GOriginal():
        return self.data[:,:,1]

    @cached_property
    def BOriginal():
        return self.data[:,:,2]

    @cached_property
    def RFlatten():
        return self.ROriginal.flatten()

    @cached_property
    def GFlatten():
        return self.ROriginal.flatten()

    @cached_property
    def BFlatten():
        return self.ROriginal.flatten()

    @cached_property
    def RGBInterlaced():
    # Byte Stream 1 - Interlacing RGBRGB (in mem viewing layout)
        interlaced = np.zeros((self.num_pixels * 3), dtype=np.half)
        for i in range(self.num_pixels):
              interlaced[i * 3] = self.RFlatten[i]
              interlaced[i * 3 + 1] = self.GFlatten[i]
              interlaced[i * 3 + 2] = self.BFlatten[i]
        return interlaced.tobytes()

    @cached_property
    def RGBSeparated():
    # Byte Stream 2 - Channel separated (RRRR...GGGG...BBBB)
        return (self.RFlatten.tobytes()
                + self.GFlatten.tobytes()
                + self.BFlatten.tobytes())

    


def ConvertAndSaveByteStreams(data, dir, fn_prefix):
    pass

def main(paths):
    for path in paths:
        try:
            data = np.load(path)
            dir, filename = os.path.split(path)
            filename_prefix, _ = os.path.splitext(filename)
            ConvertAndSaveByteStreams(data, dir, filename_prefix)
        except Exception as e:
            print(f"Could not process data file {f}.")
            print(e)

if __name__ == "__main__":
    main(sys.argv[1:])
