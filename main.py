from pathlib import Path

from block_contruction import FillDXT1_BlankPixelBlocks, DrawDXT1Graphic, FillDXT1_PixelBlocks, FillDXT4_PixelBlocks, \
    DrawDXT4Graphic, FillDXT4_BlankPixelBlocks
from sld_structure import SLD, lookup_layers


def GetCommandList(command_array):
    command_list = []
    for n in range(len(command_array)):
        command_list.append({'skip': command_array[n].skipped_blocks_count,
                             'draw': command_array[n].draw_blocks_count})
    return command_list




def ConstructMainGraphic(sld_file, current_frame, show_images=False):
    draw_commands = GetCommandList(sld_file.frames[current_frame].main.command_array)

    pixel_blocks = []
    current_block_index = 0
    for command in draw_commands:
        for skip in range(command['skip']):
            #add code here to fill from previous frame pixels

            pixel_blocks.append(FillDXT1_BlankPixelBlocks())
        for draw in range(command['draw']):
            current_block = sld_file.frames[current_frame].main.layer_blocks[current_block_index]
            lookup_table = current_block.create_lookup_table()
            pixel_blocks.append(FillDXT1_PixelBlocks(lookup_table, current_block.pixel_indices))
            current_block_index += 1

    graphics = sld_file.frames[current_frame].main.graphics_header
    width = (graphics.offset_x2 - graphics.offset_x1)
    height = (graphics.offset_y2 - graphics.offset_y1)

    MainImage = DrawDXT1Graphic(width, height, pixel_blocks)

    if show_images:
        MainImage.show()
    MainImage.save(f"images_out/main_{current_frame}.png")

    return MainImage

def ConstructDamageGraphic(sld_file, current_frame, show_images=False):

    draw_commands = GetCommandList(sld_file.frames[current_frame].damage.damage_command_array)

    pixel_blocks = []
    current_block_index = 0
    for command in draw_commands:
        for skip in range(command['skip']):
            #add code here to fill from previous frame pixels

            pixel_blocks.append(FillDXT1_BlankPixelBlocks())
        for draw in range(command['draw']):
            current_block = sld_file.frames[current_frame].damage.damage_layer_blocks[current_block_index]
            lookup_table = current_block.create_lookup_table()
            pixel_blocks.append(FillDXT1_PixelBlocks(lookup_table, current_block.pixel_indices))
            current_block_index += 1

    graphics = sld_file.frames[current_frame].main.graphics_header
    width = (graphics.offset_x2 - graphics.offset_x1)
    height = (graphics.offset_y2 - graphics.offset_y1)

    DamageImage = DrawDXT1Graphic(width, height, pixel_blocks)

    if show_images:
        DamageImage.show()
    DamageImage.save(f"images_out/damage_{current_frame}.png")

    return DamageImage

def ConstructShadowGraphic(sld_file, current_frame, show_images=False):
    draw_commands = GetCommandList(sld_file.frames[current_frame].shadow.shadow_command_array)

    pixel_blocks = []
    current_block_index = 0
    for command in draw_commands:
        for skip in range(command['skip']):
            pixel_blocks.append(FillDXT4_BlankPixelBlocks())
        for draw in range(command['draw']):
            current_block = sld_file.frames[current_frame].shadow.shadow_layer_blocks[current_block_index]
            lookup_table = current_block.create_lookup_table()

            pixel_blocks.append(FillDXT4_PixelBlocks(lookup_table, current_block.pixel_indices))
            current_block_index += 1

    graphics = sld_file.frames[current_frame].shadow.shadow_graphics_header

    width = (graphics.offset_x2 - graphics.offset_x1)
    height = (graphics.offset_y2 - graphics.offset_y1)

    ShadowImage = DrawDXT4Graphic(width, height, pixel_blocks)

    if show_images:
        ShadowImage.show()
    ShadowImage.save(f"images_out/shadow_{current_frame}.png")

    return DrawDXT4Graphic(width, height, pixel_blocks)

def ConstructPlayerColourGraphic(sld_file, current_frame, show_images=False):

    draw_commands = GetCommandList(sld_file.frames[current_frame].player_colour.player_colour_command_array)
    pixel_blocks = []
    current_block_index = 0
    for command in draw_commands:
        for skip in range(command['skip']):
            pixel_blocks.append(FillDXT4_BlankPixelBlocks())
        for draw in range(command['draw']):
            current_block = sld_file.frames[current_frame].player_colour.player_colour_layer_blocks[current_block_index]
            lookup_table = current_block.create_lookup_table()

            pixel_blocks.append(FillDXT4_PixelBlocks(lookup_table, current_block.pixel_indices))
            current_block_index += 1

    graphics = sld_file.frames[current_frame].main.graphics_header

    width = (graphics.offset_x2 - graphics.offset_x1)
    height = (graphics.offset_y2 - graphics.offset_y1)

    PlayerColourImage = DrawDXT4Graphic(width, height, pixel_blocks)

    if show_images:
        PlayerColourImage.show()
    PlayerColourImage.save(f"images_out/player_colour_{current_frame}.png")

    return DrawDXT4Graphic(width, height, pixel_blocks)

def DrawGraphicsLayers(sld_file, current_frame, show_images):
    images = {}
    frame_dict = lookup_layers(sld_file.frames[current_frame].frame_header.frame_type)
    print(frame_dict)
    images.setdefault('07 main',{})

    images['07 main'][current_frame] = ConstructMainGraphic(sld_file, current_frame, show_images)

    if frame_dict['06 shadow']:
        images.setdefault('06 shadow', {})
        images['06 shadow'] = ConstructShadowGraphic(sld_file, current_frame, show_images)
        pass

    if frame_dict['05 ???']:
        #No action known
        pass

    if frame_dict['04 damage']:
        images.setdefault('04 damage', {})
        images['04 damage'][current_frame] = ConstructDamageGraphic(sld_file, current_frame, show_images)

    if frame_dict['03 player_colour']:
        images.setdefault('03 player_colour', {})
        images['03 player_colour'][current_frame] = ConstructPlayerColourGraphic(sld_file, current_frame, show_images)

    return images

if __name__ == "__main__":


    current_sld = (Path(__file__).parent / 'sld_source/u_sie_cobra_car_idleA_x1.sld').absolute()
    current_sld = (Path(__file__).parent / 'sld_source/a_alfred_attackA_x1.sld').absolute()
    current_sld = (Path(__file__).parent / 'sld_source/s_rubble_1x1_x1.sld').absolute()
    current_sld = (Path(__file__).parent / 'sld_source/s_campfire_x1.sld').absolute()
    current_sld = (Path(__file__).parent / 'sld_source/b_scen_hut_a_x1.sld').absolute()
    current_sld = (Path(__file__).parent / 'sld_source/b_medi_castle_age3_x1.sld').absolute()

    print(f"Using file {current_sld}:")
    sld_file: SLD = SLD._from_file(str(current_sld), strict=False)

    for frame in range(sld_file.header.num_frames):
        print(frame)
        images = DrawGraphicsLayers(sld_file, frame, show_images=False)


    #Using file C:\Users\Christian\PycharmProjects\SLD\sld_source\a_alfred_attackA_x1.sld:
    #Frames present in file:  ['07 main', '06 shadow', '05 ???', '04 damage', '03 player_colour']