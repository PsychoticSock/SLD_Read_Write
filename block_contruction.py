from __future__ import annotations

from PIL import Image
from binary_file_parser import BaseStruct, Retriever
from binary_file_parser.types import uint8, uint16, uint32, Bytes

def unpack_565_color(input_color):
    # Note only returning red component to use in greyscale images
    red = (( input_color >> 11 ) & 0x1f )
    green = (( input_color >> 5 ) & 0x3f )
    blue = ( input_color & 0x1f )
    colour = []
    colour.append(( red << 3 ) | ( red >> 2 ))
    colour.append(( green << 2 ) | ( green >> 4 ))
    colour.append(( blue << 3 ) | ( blue >> 2 ))
    colour.append(255)
    return colour[0]


def FillDXT1_BlankPixelBlocks():
    return [(0,) * 4 for _ in range(16)]

def FillDXT4_BlankPixelBlocks():
    return [0] * 16

def FillDXT1_PixelBlocks(lookup_table, pixel_indices):
    pixels = []
    bitmask = 0b11

    for _ in range(16):
        bc1_idx = pixel_indices & bitmask
        pixels.append(lookup_table[bc1_idx])
        pixel_indices = pixel_indices >> 2
    return pixels


def Fill_DXT4_PixelBlocks(lookup_table, pixel_indices):
    pixels = []
    bitmask = 0b11

    pixel_indices0 = pixel_indices[0]
    for shift in range(4):
        bc4_idx = pixel_indices0 & bitmask
        col = lookup_table[bc4_idx]
        pixels.append(col)
        pixel_indices0 = pixel_indices0 >> 2

    pixel_indices1 = pixel_indices[1]
    for shift in range(4):
        bc4_idx = pixel_indices1 & bitmask
        col = lookup_table[bc4_idx]
        pixels.append(col)
        pixel_indices1 = pixel_indices1 >> 2

    pixel_indices2 = pixel_indices[2]
    for shift in range(4):
        bc4_idx = pixel_indices2 & bitmask
        col = lookup_table[bc4_idx]
        pixels.append(col)
        pixel_indices2 = pixel_indices2 >> 2

    pixel_indices3 = pixel_indices[3]
    for shift in range(4):
        bc4_idx = pixel_indices3 & bitmask
        col = lookup_table[bc4_idx]
        pixels.append(col)
        pixel_indices3 = pixel_indices3 >> 2

    return pixels


def Fill_SLD_DXT4_PixelBlocks(lookup_table, pixel_indices):
    pixels = []
    bitmask = 0b111

    pixel_indices0 = pixel_indices.v1
    for shift in range(8):
        bc4_idx = pixel_indices0 & bitmask
        col = lookup_table[bc4_idx]
        pixels.append(col)
        pixel_indices0 = pixel_indices0 >> 3

    pixel_indices1 = pixel_indices.v2
    for shift in range(8):
        bc4_idx = pixel_indices1 & bitmask
        col = lookup_table[bc4_idx]
        pixels.append(col)
        pixel_indices1 = pixel_indices1 >> 3
    return pixels

def DrawDXT1Graphic(canvas_width: int, canvas_height: int, pixel_blocks: list, from_dds_file=False):

    if from_dds_file:
        offset = 1
    else:
        offset = 0

    block_size = len(pixel_blocks[0][0])

    img = Image.new('RGBA', (canvas_width, canvas_height))
    width = canvas_width // block_size
    height = canvas_height // block_size

    for block_base_y in range(height+offset):
        for block_base_x in range(width):
            pixel_index = block_base_y * width + block_base_x
            pixels = pixel_blocks[pixel_index]

            for i, pixel in enumerate(pixels):
                x = i % 4
                y = i // 4
                if block_base_y * block_size + y < canvas_height:
                    img.putpixel((block_base_x * block_size + x, block_base_y * block_size + y), pixel)
    return img

def DrawDXT4Graphic(canvas_width: int, canvas_height: int, pixel_blocks: list, from_dds_file=False):

    if from_dds_file:
        offset = 1
    else:
        offset = 0

    block_size = 4

    img = Image.new('L', (canvas_width, canvas_height))
    width = canvas_width // block_size
    height = canvas_height // block_size

    for block_base_y in range(height+offset):
        for block_base_x in range(width):
            pixel_index = block_base_y * width + block_base_x

            pixels = pixel_blocks[pixel_index]

            for i, pixel in enumerate(pixels):
                x = i % 4
                y = i // 4
                if block_base_y * block_size + y < canvas_height:
                    img.putpixel((block_base_x * block_size + x, block_base_y * block_size + y), pixel)
    return img

class X(BaseStruct):
    _pixel_indices: bytes = Retriever(uint8, repeat = 6)

    @property
    def v1(self):
        return int.from_bytes(self._pixel_indices[:3], byteorder = 'little')

    @v1.setter
    def v1(self, value: int):
        self._pixel_indices[:3] = int.to_bytes(value, 3, byteorder = 'little')

    @property
    def v2(self):
        return int.from_bytes(self._pixel_indices[3:], byteorder = 'little')

    @v2.setter
    def v2(self, value: int):
        self._pixel_indices[3:] = int.to_bytes(value, 3, byteorder = 'little')

def to_rgb(color) -> tuple[int, int, int, int]:
    r0: int = (color & 0xF800) >> 11
    g0: int = (color & 0x07E0) >> 5
    b0: int = (color & 0x001F)
    return r0 * 8, g0 * 4, b0 * 8, 255

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

class NVTT_DXT4_Block(BaseStruct):
    AlphaDiscard: bytes = Retriever(Bytes[8])

    colorData0: int = Retriever(uint16)
    colorData1: int = Retriever(uint16)
    pixel_indices: list[int] = Retriever(uint8, repeat=4)

    def create_lookup_table(self):
        color0 = unpack_565_color(self.colorData0)
        color1 = unpack_565_color(self.colorData1)
        color2 = int(2 / 3 * color0 + 1 / 3 * color1)
        color3 = int(1 / 3 * color0 + 2 / 3 * color1)

        return [color0,
                color1,
                color2,
                color3]


class DXT4_Block(BaseStruct):
    color0: int = Retriever(uint8)
    color1: int = Retriever(uint8)
    pixel_indices: list[X] = Retriever(X)

    def create_lookup_table(self):
        rgb0 = self.color0
        rgb1 = self.color1
        rgb2 = 0
        rgb3 = 0
        rgb4 = 0
        rgb5 = 0
        rgb6 = 0
        rgb7 = 0

        if self.color0 > self.color1:
            rgb2 = int((6 * rgb0 + 1 * rgb1) / 7)
            rgb3 = int((5 * rgb0 + 2 * rgb1) / 7)
            rgb4 = int((4 * rgb0 + 3 * rgb1) / 7)
            rgb5 = int((3 * rgb0 + 4 * rgb1) / 7)
            rgb6 = int((2 * rgb0 + 5 * rgb1) / 7)
            rgb7 = int((1 * rgb0 + 6 * rgb1) / 7)

        if self.color0 <= self.color1:
            rgb2 = int((4 * rgb0 + 1 * rgb1) / 5.0)
            rgb3 = int((3 * rgb0 + 2 * rgb1) / 5.0)
            rgb4 = int((2 * rgb0 + 3 * rgb1) / 5.0)
            rgb5 = int((1 * rgb0 + 4 * rgb1) / 5.0)
            rgb6 = 0
            rgb7 = 255

        return [rgb0,
                rgb1,
                rgb2,
                rgb3,
                rgb4,
                rgb5,
                rgb6,
                rgb7]
