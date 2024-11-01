from local_files import aoe2_path


def GetPalette(filename):
    with open(filename) as file:
        lines = [line.rstrip().split(" ") for line in file]

    #palette_colour_count = int(lines[2][0])
    rgb_list =[{"red":line[0], "green":line[1], "blue":line[2], "alpha":line[3]} for line in lines[3:]]
    return rgb_list

class Palette:
    '''This stores rgba data from a palette to interpret SMX files'''

    def __init__(self, palette_number, filename):
        self.palette_number = palette_number

        self.filename = filename
        with open(filename) as file:
            lines = [line.rstrip().split(" ") for line in file if len(line) > 1]
            if len(lines[3]) < 3:
                starting_rgb = 4
            else:
                starting_rgb = 3
            if len(lines[starting_rgb]) == 3:
                self.alpha_channel = False
                rgb_list = [[line[0], line[1], line[2]] for line in lines[starting_rgb:]]
            else:
                self.alpha_channel = True
                rgb_list = [[line[0], line[1], line[2], line[3]] for line in lines[starting_rgb:] if len(line)>1]

            self.palette_color_count = int(lines[2][0])

        self.colours = rgb_list

    def get_colour(self, palette_section, colour_index):

        return self.colours[int(palette_section * 256) + colour_index]

def get_palettes():
    palettes = []
    with open(fr"{aoe2_path}\resources\_common\palettes\palettes.conf") as file:
        lines = [line.rstrip().split(",") for line in file if line[0].isdigit()]
        for line in lines:
            palettes.append([line[0], fr"{aoe2_path}\resources\_common\palettes\{line[1]}"])
        return (palettes)

palette_list = get_palettes()

def fill_palettes():
    palettes = {}
    for palette_number, filename in palette_list:
        palettes.setdefault(palette_number, Palette(palette_number, filename))
    return palettes


my_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

for x, item in enumerate(range(0, len(my_list), 5)):
    pixels = my_list[x*5:x*5 + 5]
    pixel0 = pixels[0]
    pixel1 = pixels[1]
    pixel2 = pixels[2]
    pixel3 = pixels[3]
    palette_sections = pixels[4]
    print(format(palette_sections, '010b'))
    palette_section_pixel0 = palette_sections & 0b00000011
    palette_section_pixel1 = palette_sections >> 2 & 0b00000011
    palette_section_pixel2 = palette_sections >> 4 & 0b00000011
    palette_section_pixel3 = palette_sections >> 6 & 0b00000011


    print(format(palette_section_pixel0, '010b'), format(palette_section_pixel1, '010b'), format(palette_section_pixel2, '010b'), format(palette_section_pixel3, '010b'))
    print(palette_section_pixel0, palette_section_pixel1, palette_section_pixel2, palette_section_pixel3)

#print(palette1.get_colour(3, 0))
