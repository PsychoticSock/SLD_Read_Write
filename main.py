from local_files import current_sld
from sld_structure import SLD
from PIL import Image
import numpy as np


sld_file:SLD = SLD.from_file(current_sld, strict=False)

#### https://github.com/bensnell/stb_dxt


def to_rgb(color):
    r0 = (color & 0xF800) >> 11
    g0 = (color & 0x07E0) >> 5
    b0 = (color & 0x001F)
    return ((r0,g0,b0, 1)) #Now in RGBA16 format

def interpolate_colour(color0, color1):

    lookup_table = [None] * 4
    lookup_table[0] = to_rgb(color0)
    lookup_table[1] = to_rgb(color1)

    if color0>color1:
        color2 = to_rgb(int((2 / 3) * color0 + (1 / 3) * color1))
        color3 = to_rgb(int((1 / 3) * color0 + (2 / 3) * color1))

    else:
        color2 = to_rgb(int((1 / 2) * color0 + (1 / 2) * color1))
        color3 = (0, 0, 0, 0)

    lookup_table[2] = color2
    lookup_table[3] = color3

    return (lookup_table)


def FillDXT1_PixelBlocks(lookup_table, pixel_indices):
    pixels = []
    bitmask = 0b11
    for shift in range(16):
        bc1_idx = pixel_indices & bitmask
        col = lookup_table[bc1_idx]
        pixels.append(col)
        pixel_indices = pixel_indices >> 2
    pixels = np.array_split(pixels, 4)
    return pixels

def DrawMainGraphicBlock(pixels):
    img = Image.new('RGB', (4, 4))
    for y, pixel_row in enumerate(pixels):
        for x, pixel in enumerate(pixel_row):
            img.putpixel((x,y), tuple(pixel))
    return img

if __name__ == "__main__":


    for block_no, block in enumerate(sld_file.layer_blocks):
        if  block_no == 50: # limited to one block to test what was written at the moment
            lookup_table = interpolate_colour(block.color0, block.color1)
            pixels = FillDXT1_PixelBlocks(lookup_table, block.pixel_indices)
            TestImage = DrawMainGraphicBlock(pixels)
            #TestImage.show()
            TestImage.save("TEST_IMG.png")

    #print(sld_file)
