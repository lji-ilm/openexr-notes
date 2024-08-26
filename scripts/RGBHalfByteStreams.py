from functools import cached_property

import numpy as np


def SeparateHiLow(bstream):
    x0 = bytearray()
    x1 = bytearray()
    for i in range(len(bstream)):
        if i % 2 == 0:
            x0.append(bstream[i])
        else:
            x1.append(bstream[i])
    # choose endian
    # return bytes(x0), bytes(x1)
    return bytes(x1), bytes(x0)


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


class RGBHalfByteStreams():
    def __init__(self, RGBData):
        assert RGBData.dtype == np.half
        shape = RGBData.shape
        assert shape[2] >= 3

        self.width = shape[0]
        self.height = shape[1]
        self.num_pixels = self.width * self.height
        self.data = RGBData

    @cached_property
    def ROriginal(self):
        return self.data[:, :, 0]

    @cached_property
    def GOriginal(self):
        return self.data[:, :, 1]

    @cached_property
    def BOriginal(self):
        return self.data[:, :, 2]

    @cached_property
    def RFlatten(self):
        return self.ROriginal.flatten()

    @cached_property
    def GFlatten(self):
        return self.GOriginal.flatten()

    @cached_property
    def BFlatten(self):
        return self.BOriginal.flatten()

    @cached_property
    def RGBInterlaced(self):
        # Byte Stream 1 - Interlacing RGBRGB (in mem viewing layout)
        interlaced = np.zeros((self.num_pixels * 3), dtype=np.half)
        for i in range(self.num_pixels):
            interlaced[i * 3] = self.RFlatten[i]
            interlaced[i * 3 + 1] = self.GFlatten[i]
            interlaced[i * 3 + 2] = self.BFlatten[i]
        return interlaced.tobytes()

    @cached_property
    def RGBSeparated(self):
        # Byte Stream 2 - Channel separated (RRRR...GGGG...BBBB)
        return (self.ROriginal.tobytes()
                + self.GOriginal.tobytes()
                + self.BOriginal.tobytes())

    @cached_property
    def RHiLo(self):
        return SeparateHiLow(self.ROriginal.tobytes())

    @cached_property
    def GHiLo(self):
        return SeparateHiLow(self.GOriginal.tobytes())

    @cached_property
    def BHiLo(self):
        return SeparateHiLow(self.BOriginal.tobytes())

    @cached_property
    def ByteSwizzled(self):
        # Byte Stream 3 - Byte Swizzled (R_hi R_hi R_hi ... R_lo R_lo R_lo).
        return (self.RHiLo[0] + self.RHiLo[1]
                + self.GHiLo[0] + self.GHiLo[1]
                + self.BHiLo[0] + self.BHiLo[1])

    @cached_property
    def ByteSwizzledDelta(self):
        # Byte Stream 4 - Byte Swizzled + Delta encoding.
        return DeltaEncode(self.ByteSwizzled)

    @cached_property
    def RHiPredicted(self):
        R_hi = self.RHiLo[0]
        G_hi = self.GHiLo[0]
        return predict(R_hi, G_hi)

    @cached_property
    def BHiPredicted(self):
        B_hi = self.BHiLo[0]
        G_hi = self.GHiLo[0]
        return predict(B_hi, G_hi)

    @cached_property
    def RBPredicted(self):
        # Byte Stream 5 - Channel Correlation Prediction - R_exp and B_exp are predicted.
        # Note that here we only predict the exponoent byte.
        return (self.GHiLo[0] + self.GHiLo[1]
                + self.RHiPredicted + self.RHiLo[1]
                + self.BHiPredicted + self.BHiLo[1])

    @cached_property
    def RBPredictedDelta(self):
        # Byte Stream 6 - Channel Correlation Prediction + Delta encoding.
        return DeltaEncode(self.RBPredicted)

    @cached_property
    def RLoPredicted(self):
        R_lo = self.RHiLo[1]
        G_lo = self.GHiLo[1]
        return predict(R_lo, G_lo)

    @cached_property
    def BLoPredicted(self):
        B_lo = self.BHiLo[1]
        G_lo = self.GHiLo[1]
        return predict(B_lo, G_lo)

    @cached_property
    def RBHiLoPredicted(self):
        # Byte Stream 6 - Both exp and mantissa bytes on R and B are predicted
        return (self.GHiLo[0] + self.GHiLo[1]
                + self.RHiPredicted + self.RLoPredicted
                + self.BHiPredicted + self.BLoPredicted)

    @cached_property
    def RBHiLoPredictedDelta(self):
        # Byte Stream 7 - Delta encoding on stream 6
        return DeltaEncode(self.RBHiLoPredicted)
