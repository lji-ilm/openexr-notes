import os
import sys
from functools import cached_property

import numpy as np

def SeparateHiLow(bstream):
    hi = bytearray()
    low = bytearray()
    for i in range(len(bstream)):
        if i % 2 == 0:
            hi.append(bstream[i])
        else:
            low.append(bstream[i])

    return bytes(hi), bytes(low)

def DeltaEncode(bstream):
    delta = bytearray()
    prev = 0
    for i in range(len(bstream)):
        d = bstream[i] - prev
    if d >= 0:
        delta.append(d)
    else:
        delta.append(d + 256)
    prev = bstream[i]

    return bytes(delta)

def predict(bstream, pivot):
    residue = bytearray()
    for i in range(len(bstream)):
        r = bstream[i] - pivot[i]
        if r < 0:
            r += 256
        residue.append(r)

    return bytes(residue)

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
        return (self.ROriginal.tobytes()
                + self.GOriginal.tobytes()
                + self.BOriginal.tobytes())

    @cached_property
    def RHiLo():
        return SeparateHiLow(self.ROriginal.tobytes())

    @cached_property
    def GHiLo():
        return SeparateHiLow(self.GOriginal.tobytes())

    @cached_property
    def BHiLo():
        return SeparateHiLow(self.BOriginal.tobytes())

    @cached_property
    def ByteSwizzled():
    # Byte Stream 3 - Byte Swizzled (R_hi R_hi R_hi ... R_low R_low R_low).
        return (self.RHiLo[0] + self.RHiLo[1]
                + self.GHiLo[0] + self.GHiLo[1]
                + self.BHiLo[0] + self.BHiLo[1])
    
    @cached_property
    def ByteSwizzeldDelta():
    # Byte Stream 4 - Byte Swizzled + Delta encoding.
        return DeltaEncode(self.ByteSwizzled)

    @cached_property
    def RHiPredicted():
        R_hi = self.RHiLo[0]
        G_hi = self.GHiLo[0]
        return predict(R_hi, G_hi)
    
    @cached_property
    def BHiPredicted():
        B_hi = self.BHiLo[0]
        G_hi = self.GHiLo[0]
        return predict(B_hi, G_hi)

    @cached_property
    def RBPredicted():
    # Byte Stream 5 - Channel Correlation Prediction - R_exp and B_exp are predicted.
    # Note that here we only predict the exponoent byte.
        return (self.GHiLo[0] + self.GHiLo[1]
                + self.RHiPredicted + self.RHiLo[1]
                + self.BHiPredicted + self.BHiLo[1])

    @cached_property
    def RBPredictedDelta():
    # Byte Stream 6 - Channel Correlation Prediction + Delta encoding.
        return DeltaEncode(self.RBPredicted)

    @cached_property
    def RLoPredicted():
        R_lo = self.RHiLo[1]
        G_lo = self.GHiLo[1]
        return predict(R_lo, G_lo)

    @cached_property
    def BLoPredicted():
        B_lo = self.BHiLo[1]
        G_lo = self.GHiLo[1]
        return predict(B_lo, G_lo)

    @cached_property
    def RBHiLoPredicted():
    # Byte Stream 6 - Both exp and mantissa bytes on R and B are predicted
        return (self.GHiLo[0] + self.GHiLo[1]
                + self.RHiPredicted + self.RLoPredicted
                + self.BHiPredicted + self.BLoPredicted)

    @cached_property
    def RBHiLoPredictedDelta():
    # Byte Stream 7 - Delta encoding on stream 6
        return DeltaEncode(self.RBHiLoPredicted)

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
