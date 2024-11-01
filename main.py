from pathlib import Path
from PIL import Image

from SLD_drawing import DrawGraphicsLayers
from SLD_struct.sld_structure import SLD
from SMX_struct.palette import GetPalette, fill_palettes
from SMX_struct.smx_structure import SMX, convert_pixel_array_to_lookup, SMP_Layer_Row_Edge

cmdSkip = "cmdSkip"
cmdDraw = "cmdDraw"
cmdPlayerColour = "cmdPlayerColour"
cmdEnd = "cmdEnd"

def show_smx_command_type(command):
    if command == 0:
        return "cmdSkip"
    if command == 1:
        return "cmdDraw"
    if command == 2:
        return "cmdPlayerColour"
    if command == 3:
        return "cmdEnd"


if __name__ == "__main__":

    current_sld = (Path(__file__).parent / 'sld_source/u_sie_cobra_car_idleA_x1.sld').absolute()
    current_sld = (Path(__file__).parent / 'sld_source/s_rubble_1x1_x1.sld').absolute()
    current_sld = (Path(__file__).parent / 'sld_source/b_scen_hut_a_x1.sld').absolute()
    current_sld = (Path(__file__).parent / 'sld_source/s_campfire_x1.sld').absolute()
    current_sld = (Path(__file__).parent / 'sld_source/a_alfred_attackA_x1.sld').absolute()
    current_sld = (Path(__file__).parent / 'sld_source/b_medi_castle_age3_x1.sld').absolute()


    current_smx = (Path(__file__).parent / 'smx_source/b_scen_hut_a_x1.smx').absolute()
    current_smx = (Path(__file__).parent / 'smx_source/s_rubble_1x1_x1.smx').absolute()
    current_smx = (Path(__file__).parent / 'smx_source/a_alfred_attackA_x1.smx').absolute()
    current_smx = (Path(__file__).parent / 'smx_source/b_medi_castle_age3_x1.smx').absolute()
    current_smx = (Path(__file__).parent / 'smx_source/u_sie_cobra_car_idleA_x1.smx').absolute()
    current_smx = (Path(__file__).parent / 'smx_source/smx_test_tiny.smx').absolute()
    current_smx = (Path(__file__).parent / 'smx_source/test_colours.smx').absolute()
    current_smx = (Path(__file__).parent / 'smx_source/player_colour_test.smx').absolute()
    current_smx = (Path(__file__).parent / 'smx_source/s_campfire_x1.smx').absolute()

SLD_test = False
if SLD_test:
    print(f"Using file {current_sld}:")
    sld_file: SLD = SLD._from_file(str(current_sld), strict=False)

    for frame in range(sld_file.sld_header.num_frames):
        #print(frame)
        images = DrawGraphicsLayers(sld_file, frame, show_images=False)


SMX_test = True
if SMX_test:
    print(f"Using file {current_smx}:")

    smx_file: SMX = SMX._from_file(str(current_smx), strict=True)
    print(smx_file)

    palette_used = smx_file.smx_frames[0].smx_frame_header.palette_number
    print(palette_used)

    width = smx_file.smx_frames[0].smx_main.layer_header.width
    height = smx_file.smx_frames[0].smx_main.layer_header.height
    img = Image.new('RGBA', (width, height))

    output = []
    palettes = fill_palettes()



    current_pixel_index = 0

    for row_no, edge_data in enumerate(smx_file.smx_frames[0].smx_main.smp_layer_row_edge):  # type: SMP_Layer_Row_Edge
        for pixel_count in range(edge_data.left_space):
            print("left", pixel_count)
            #output.append([0, 0, 0, 0])

        for pixel_count in range(edge_data.right_space):
            print("right", pixel_count)
            #output.append([0, 0, 0, 0])


    for command_array_index, command in enumerate(smx_file.smx_frames[0].smx_main.command_array):
        current_pixels = convert_pixel_array_to_lookup(smx_file.smx_frames[0].smx_main.pixel_data_array)
        command_bitmask = 0b00000011

        # print("main", frame_type & main_bitmask)
        command_type = show_smx_command_type(command & command_bitmask)
        pixel_count = (command >> 2)+1

        print(f"Command Count {len(smx_file.smx_frames[0].smx_main.command_array)}, Pixel_array_length {smx_file.smx_frames[0].smx_main.pixel_data_array_length}, Command_Index {command_array_index}, Command:{bin(command)}, type:{command_type} ,Pixel Count:{pixel_count}")

        #print("Pixels", len(smx_file.smx_frames[0].smx_main.pixel_data_array))
        for command_repeat_count in range(pixel_count):
        #    print("current_pixel = ", smx_file.smx_frames[0].smx_main.pixel_data_array[command_counter], "command_counter ", command_counter)
            if command_type == cmdSkip:
                output.append([0, 0, 0, 0])
                #Debug Print# print("SKIPPED")
            if command_type == cmdDraw:
                #Debug Print# print("DRAW")
                #Debug Print# print("Pixel data", current_pixels[current_pixel_index])
                current_pixel_rgb = palettes[str(palette_used)].get_colour(current_pixels[current_pixel_index][1], current_pixels[current_pixel_index][0])
                #Debug Print# print(current_pixel_rgb)
                output.append(current_pixel_rgb)
                current_pixel_index += 1
            if command_type == cmdPlayerColour:
                #Debug Print# print("PLAYER_COLOUR")
                #Debug Print# print(current_pixels[current_pixel_index])
                output.append([0, 0, 0, 255]) # Placeholder for player colour for now
                current_pixel_index += 1
            if command_type == cmdEnd:
                print("END")
    print(output)
    for y in range(height):
        for x in range(width):
            #try:
            #Debug Print# print(f"x: {x}, y:{y}, width:{width}, height:{height},  output_length:{len(output)}")
            location = (x, y)
            try:
                output_pixel = (tuple(output[y * width + x]))
                #Debug Print# print("location", location, "output_pixel", output_pixel)
                int_pixel = (int(output_pixel[0]),
                             int(output_pixel[1]),
                             int(output_pixel[2]),
                             int(output_pixel[3]))
                #Debug Print# print(int_pixel)
                img.putpixel(location, int_pixel)

            except:
                #Debug Print# print(f"error at {x, y}")
                pass

    img.save("test_smx_png.png")
    #img.show()

    #palette_colours = (GetPalette(r"C:\Users\Christian\PycharmProjects\SLD\smx_source\b_seas.pal"))

    #img = Image.new('RGBA', (32, 32))
    #pixel_index = 0
    #for y in range(32):
    #    for x in range(32):
    #        current_pixel = (int(palette_colours[pixel_index]['red']), int(palette_colours[pixel_index]['green']), int(palette_colours[pixel_index]['blue']), int(palette_colours[pixel_index]['alpha']))
    #        print(current_pixel, (pixel_index))
    #        img.putpixel((x, y), current_pixel)
    #        pixel_index += 1
    #new_img = img.resize(size=(1024,1024), resample=Image.Resampling.BOX)
    ##new_img.show()
    #new_img.save("test_palette.png")
