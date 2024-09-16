from pathlib import Path

from block_contruction import FillDXT1_BlankPixelBlocks, DrawDXT1Graphic, FillDXT1_PixelBlocks, FillDXT4_PixelBlocks, \
    DrawDXT4Graphic, FillDXT4_BlankPixelBlocks
from sld_structure import SLD

def GetCommandList(command_array):
    command_list = []
    for n in range(len(command_array)):
        command_list.append({'skip': command_array[n].skipped_blocks_count,
                             'draw': command_array[n].draw_blocks_count})
    return command_list


def lookup_layers(frame_type):
    frames = bin(frame_type)[2:].zfill(8)
    result = {}
    result['03 player_colour'] = int(frames[3])
    result['04 damage'] = int(frames[4])
    result['05 ???'] = int(frames[5])
    result['06 shadow'] = int(frames[6])
    result['07 main'] = int(frames[7])
    print("Frames present in file: ", list(reversed(sorted(result.keys()))))
    return result

def ConstructMainGraphic(sld_file, show_images=False):
    draw_commands = GetCommandList(sld_file.command_array)

    pixel_blocks = []
    current_block_index = 0
    for command in draw_commands:
        for skip in range(command['skip']):
            pixel_blocks.append(FillDXT1_BlankPixelBlocks())
        for draw in range(command['draw']):
            current_block = sld_file.layer_blocks[current_block_index]
            lookup_table = current_block.create_lookup_table()
            pixel_blocks.append(FillDXT1_PixelBlocks(lookup_table, current_block.pixel_indices))
            current_block_index += 1

    graphics = sld_file.graphics_header
    width = (graphics.offset_x2 - graphics.offset_x1)
    height = (graphics.offset_y2 - graphics.offset_y1)

    MainImage = DrawDXT1Graphic(width, height, pixel_blocks)

    if show_images:
        MainImage.show()
    MainImage.save("images_out/main.png")

    return MainImage


def ConstructShadowGraphic(sld_file, show_images=False):
    draw_commands = GetCommandList(sld_file.shadow_command_array)

    pixel_blocks = []
    current_block_index = 0
    for command in draw_commands:
        for skip in range(command['skip']):
            pixel_blocks.append(FillDXT4_BlankPixelBlocks())
        for draw in range(command['draw']):
            current_block = sld_file.shadow_layer_blocks[current_block_index]
            lookup_table = current_block.create_lookup_table()

            pixel_blocks.append(FillDXT4_PixelBlocks(lookup_table, current_block.pixel_indices))
            current_block_index += 1

    graphics = sld_file.shadow_graphics_header

    width = (graphics.offset_x2 - graphics.offset_x1)
    height = (graphics.offset_y2 - graphics.offset_y1)

    ShadowImage = DrawDXT4Graphic(width, height, pixel_blocks)

    if show_images:
        ShadowImage.show()
    ShadowImage.save("images_out/shadow.png")

    return DrawDXT4Graphic(width, height, pixel_blocks)

def DrawGraphicsLayers(sld_file, show_images=False):
    images = {}
    frame_dict = lookup_layers(sld_file.frame_header.frame_type)

    images['07 main'] = ConstructMainGraphic(sld_file, show_images=show_images)

    if frame_dict['06 shadow']:
        images['06 shadow'] = ConstructShadowGraphic(sld_file, show_images=show_images)
        pass

    if frame_dict['05 ???']:
        #No action known
        pass

    if frame_dict['04 damage']:
        #Implement DXT1 algorithm for this layer
        pass

    if frame_dict['03 player_colour']:
        #Implement DXT4 algorithm for this layer
        pass


    return images

if __name__ == "__main__":

    current_sld = (Path(__file__).parent / 'sld_source/b_medi_castle_age3_x1.sld').absolute()
    current_sld = (Path(__file__).parent / 'sld_source/s_campfire_x1.sld').absolute()
    current_sld = (Path(__file__).parent / 'sld_source/b_scen_hut_a_x1.sld').absolute()
    current_sld = (Path(__file__).parent / 'sld_source/s_rubble_1x1_x1.sld').absolute()
    current_sld = (Path(__file__).parent / 'sld_source/a_alfred_attackA_x1.sld').absolute()
    current_sld = (Path(__file__).parent / 'sld_source/b_medi_castle_age3_x1.sld').absolute()

    sld_file: SLD = SLD._from_file(str(current_sld), strict=False)

    images = DrawGraphicsLayers(sld_file, show_images=False)
