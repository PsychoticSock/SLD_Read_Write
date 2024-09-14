from __future__ import annotations

from binary_file_parser import BaseStruct, Retriever
from binary_file_parser.types import uint8, uint16, uint32, FixedLenStr


def to_rgb(color) -> tuple[int, int, int, int]:
    r0: int = (color & 0xF800) >> 11
    g0: int = (color & 0x07E0) >> 5
    b0: int = (color & 0x001F)
    # return r0, g0, b0, 1  #Now in RGBA16 format
    return r0 * 8, g0 * 4, b0 * 8, 255

def to_rgb_gray(color) -> tuple[int, int, int, int]:
    r0: int = color
    g0: int = 0
    b0: int = 0
    # return r0, g0, b0, 1  #Now in RGBA16 format
    return r0, g0, b0, 255


class DXT1_Block(BaseStruct):
    color0: int = Retriever(uint16)
    color1: int = Retriever(uint16)
    pixel_indices: int = Retriever(uint32)

    def create_lookup_table(self):
        rgb0 = to_rgb(self.color0)
        rgb1 = to_rgb(self.color1)
        rgb2 = [0, 0, 0, 255]
        rgb3 = [0, 0, 0, 255]

        for i in range(3):
            if self.color0 > self.color1:
                rgb2[i] = int((2 / 3) * rgb0[i] + (1 / 3) * rgb1[i])
                rgb3[i] = int((1 / 3) * rgb0[i] + (2 / 3) * rgb1[i])
            else:
                rgb2[i] = int((1 / 2) * rgb0[i] + (1 / 2) * rgb1[i])
                rgb3[i] = 0

        if self.color0 <= self.color1:
            rgb3[3] = 0

        return [
            tuple(rgb) for rgb in [rgb0, rgb1, rgb2, rgb3]
        ]


class DXT4_Block(BaseStruct):
    color0: int = Retriever(uint8)
    color1: int = Retriever(uint8)
    pixel_indices: str = Retriever(FixedLenStr[6])

    def create_lookup_table(self):

        rgb0 = to_rgb_gray(self.color0)
        rgb1 = to_rgb_gray(self.color1)
        rgb2 = [0, 0, 0, 255]
        rgb3 = [0, 0, 0, 255]
        rgb4 = [0, 0, 0, 255]
        rgb5 = [0, 0, 0, 255]
        rgb6 = [0, 0, 0, 255]
        rgb7 = [0, 0, 0, 255]

        if self.color0 > self.color1:
            rgb2[0] = int((6 * rgb0[0] + 1 * rgb1[0]) / 7)
            rgb3[0] = int((5 * rgb0[0] + 2 * rgb1[0]) / 7)
            rgb4[0] = int((4 * rgb0[0] + 3 * rgb1[0]) / 7)
            rgb5[0] = int((3 * rgb0[0] + 4 * rgb1[0]) / 7)
            rgb6[0] = int((2 * rgb0[0] + 5 * rgb1[0]) / 7)
            rgb7[0] = int((1 * rgb0[0] + 6 * rgb1[0]) / 7)

        if self.color0 <= self.color1:
            rgb2[0] = int((4 * rgb0[0] + 1 * rgb1[0]) / 5.0)
            rgb3[0] = int((3 * rgb0[0] + 2 * rgb1[0]) / 5.0)
            rgb4[0] = int((2 * rgb0[0] + 3 * rgb1[0]) / 5.0)
            rgb5[0] = int((1 * rgb0[0] + 4 * rgb1[0]) / 5.0)
            rgb6[0] = 0
            rgb7[0] = 255

        return [rgb0,
                rgb1,
                tuple(rgb2),
                tuple(rgb3),
                tuple(rgb4),
                tuple(rgb5),
                tuple(rgb6),
                tuple(rgb7)]


class CommandArray(BaseStruct):
    skipped_blocks_count: int = Retriever(uint8)
    draw_blocks_count: int = Retriever(uint8)


class GraphicsHeader(BaseStruct):
    offset_x1: int = Retriever(uint16, default=0)
    offset_y1: int = Retriever(uint16, default=0)
    offset_x2: int = Retriever(uint16, default=0)
    offset_y2: int = Retriever(uint16, default=0)
    flag1: int = Retriever(uint8, default=0)
    unknown1: int = Retriever(uint8, default=0)


class LayerData(BaseStruct):
    pass
