import math
from pathlib import Path

from layer_data import DXT1_Block
from sld_structure import SLD
from PIL import Image


def FillDXT1_BlankPixelBlocks():
    pixels = [(0,) * 4 for _ in range(16)]
    #print("Blank_pixels", pixels)
    return pixels

def FillDXT4_BlankPixelBlocks():
    pixels = [(0,) * 4 for _ in range(16)]
    #print("Blank_pixels", pixels)
    return pixels

def FillDXT1_PixelBlocks(lookup_table, pixel_indices):
    pixels = []
    bitmask = 0b11
    for _ in range(16):
        bc1_idx = pixel_indices & bitmask
        pixels.append(lookup_table[bc1_idx])
        pixel_indices = pixel_indices >> 2
    return pixels


def FillDXT4_PixelBlocks(lookup_table, pixel_indices):

    pixels = []
    bitmask = 0b111
    pixel_indices0 = pixel_indices[0:3]
    for shift in range(8):
        bc4_idx = pixel_indices0 & bitmask
        col = lookup_table[bc4_idx]
        pixels.append(col)
        pixel_indices0 = pixel_indices0 >> 3

    pixel_indices1 = pixel_indices[3:6]
    for shift in range(8):
        bc4_idx = pixel_indices1 & bitmask
        col = lookup_table[bc4_idx]
        pixels.append(col)
        pixel_indices1 = pixel_indices1 >> 3
    return pixels



def DrawMainGraphic(width: int, height: int, pixel_blocks: list):
    block_size = len(pixel_blocks[0][0])

    if width % block_size != 0 or height % block_size != 0:
        raise ValueError(f"Width and height must be multiples of {block_size}")

    img = Image.new('RGBA', (width, height))

    width = width // block_size
    height = height // block_size

    for block_base_y in range(height):
        for block_base_x in range(width):
            pixel_index = block_base_y * width + block_base_x

            pixels = pixel_blocks[pixel_index]

            for i, pixel in enumerate(pixels):
                x = i % 4
                y = i // 4
                #print("pixel", pixel)
                img.putpixel((block_base_x * block_size + x, block_base_y * block_size + y), pixel)

    return img

def DrawShadowGraphic(width: int, height: int, pixel_blocks: list):
    block_size = len(pixel_blocks[0][0])

    if width % block_size != 0 or height % block_size != 0:
        raise ValueError(f"Width and height must be multiples of {block_size}")

    img = Image.new('L', (width, height))

    width = width // block_size
    height = height // block_size

    for block_base_y in range(height):
        for block_base_x in range(width):
            pixel_index = block_base_y * width + block_base_x

            pixels = pixel_blocks[pixel_index]

            for i, pixel in enumerate(pixels):
                x = i % 4
                y = i // 4
                #print("pixel", pixel)
                img.putpixel((block_base_x * block_size + x, block_base_y * block_size + y), pixel)

    return img

def GetCommandList(command_array):
    command_list = []
    for n in range(len(command_array)):
        command_list.append({'skip': command_array[n].skipped_blocks_count,
                             'draw': command_array[n].draw_blocks_count})
    return command_list

def lookup_layers(frame_type):
    result = {}
    result['player_colour'] = int(frame_type[3])
    result['damage'] = int(frame_type[4])
    result['???'] = int(frame_type[5])
    result['main'] = int(frame_type[6])
    result['shadow'] = int(frame_type[7])
    return result

def MainGraphicStart(sld_file):
    draw_commands = GetCommandList(sld_file.command_array)

    pixel_blocks = []
    current_block_index = 0
    for command in draw_commands:
        # print(command['skip'], command['draw'])
        for skip in range(command['skip']):
            pixel_blocks.append(FillDXT1_BlankPixelBlocks())
        for draw in range(command['draw']):
            current_block = sld_file.layer_blocks[current_block_index]
            lookup_table = current_block.create_lookup_table()
            print("current_block.pixel_indices", current_block.pixel_indices, type(current_block.pixel_indices))
            pixel_blocks.append(FillDXT1_PixelBlocks(lookup_table, current_block.pixel_indices))
            current_block_index += 1

    graphics = sld_file.graphics_header

    width = (graphics.offset_x2 - graphics.offset_x1)
    height = (graphics.offset_y2 - graphics.offset_y1)

    TestMainImage = DrawMainGraphic(width, height, pixel_blocks)

    return TestMainImage

def ShadowGraphicStart(sld_file):
    draw_commands = GetCommandList(sld_file.command_array)

    pixel_blocks = []
    current_block_index = 0
    for command in draw_commands:
        # print(command['skip'], command['draw'])
        for skip in range(command['skip']):
            pixel_blocks.append(FillDXT4_BlankPixelBlocks())
        for draw in range(command['draw']):
            current_block = sld_file.shadow_layer_blocks[current_block_index]
            lookup_table = current_block.create_lookup_table()
            print("lookuptable:", lookup_table)
            print("current_block.pixel_indices", current_block.pixel_indices, type(current_block.pixel_indices))
            pixel_blocks.append(FillDXT4_PixelBlocks(lookup_table, current_block.pixel_indices))
            current_block_index += 1

    graphics = sld_file.graphics_header

    width = (graphics.offset_x2 - graphics.offset_x1)
    height = (graphics.offset_y2 - graphics.offset_y1)

    TestShadowImage = DrawShadowGraphic(width, height, pixel_blocks)

    return TestShadowImage


if __name__ == "__main__":

    current_sld = (Path(__file__).parent / 'b_medi_castle_age3_x1.sld').absolute()
    current_sld = (Path(__file__).parent / 's_campfire_x1.sld').absolute()
    current_sld = (Path(__file__).parent / 'b_scen_hut_a_x1.sld').absolute()
    current_sld = (Path(__file__).parent / 's_rubble_1x1_x1.sld').absolute()
    current_sld = (Path(__file__).parent / 'a_alfred_attackA_x1.sld').absolute()
    current_sld = (Path(__file__).parent / 'b_medi_castle_age3_x1.sld').absolute()

    sld_file: SLD = SLD._from_file(str(current_sld), strict=False)

    frame_type = bin(sld_file.frame_header.frame_type)[2:].zfill(8)
    print("Frame Type", frame_type)
    frame_dict = lookup_layers(frame_type)
    print(frame_dict)

    TestMainImage = MainGraphicStart(sld_file)

    if frame_dict['shadow']:
        TestShadowImage = ShadowGraphicStart(sld_file)
        pass

    if frame_dict['???']:
        #No action known
        pass

    if frame_dict['damage']:
        #Implement DXT1 algorithm for this layer
        pass

    if frame_dict['player_colour']:
        #Implement DXT4 algorithm for this layer
        pass

    TestMainImage.show()
    TestMainImage.save("TEST_IMG.png")
    TestShadowImage.show()
    TestShadowImage.save("TEST_SHADOW_IMG.png")

    #print(sld_file)

