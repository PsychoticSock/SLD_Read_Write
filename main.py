from pathlib import Path
from PIL import Image

from SLD_drawing import DrawGraphicsLayers
from SLD_struct.sld_structure import SLD
from SMX_struct.palette import GetPalette, fill_palettes
from SMX_struct.smx_structure import SMX

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
    current_smx = (Path(__file__).parent / 'smx_source/test_colours.smx').absolute()
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
    width = smx_file.smx_frames[0].smx_main.layer_header.width
    height = smx_file.smx_frames[0].smx_main.layer_header.height
    img = Image.new('RGBA', (width, height))
    output = []
    for command in smx_file.smx_frames[0].smx_main.command_array:
        command_bitmask = 0b00000011

        # print("main", frame_type & main_bitmask)
        command_type = show_smx_command_type(command & command_bitmask)
        pixel_count = (command >> 2)+1

        print(f"Command:{bin(command)}, type:{command_type} ,Pixel Count:{pixel_count}")

        if command_type == cmdSkip:
            output.append([0, 0, 0, 0])
        if command_type == cmdDraw:
            for pixels in (smx_file.smx_frames[0].smx_main.pixel_data_array[0:5]):
                print("compression", smx_file.smx_frames[0].compression_8_to_5)
                print(pixels)
                palette_used = smx_file.smx_frames[0].smx_frame_header.palette_number
                print("palette_used", palette_used)
                #print(bin(pixels << 24))
                print(pixels)
                print(pixels)

    fill_palettes()
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
