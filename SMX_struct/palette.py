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
        return self.colours[(palette_section * 256) + colour_index]

def get_palettes():
    palettes = []
    with open(fr"{aoe2_path}\resources\_common\palettes\palettes.conf") as file:
        lines = [line.rstrip().split(",") for line in file if line[0].isdigit()]
        for line in lines:
            palettes.append([line[0], fr"{aoe2_path}\resources\_common\palettes\{line[1]}"])
        return (palettes)

palette_list = get_palettes()
palettes = []

def fill_palettes():
    for palette_number, filename in palette_list:
        palettes.append(Palette(palette_number, filename))


#print(palette1.get_colour(3, 0))
