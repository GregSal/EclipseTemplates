from pathlib import Path
structures_path = Path(r'\\dkphysicspv1\e$\Gregs_Work\Eclipse\Version 13 upgrade\Structure Dictionary')
color_file = structures_path / 'ColorNames.csv'
color_data = str(color_file.read_text())
colors = color_data.split(sep='\n')
colors.pop()
class colour(object):
    '''colour definition'''
    def __init__(self, name, red, green, blue):
        '''define the colour from its RGB components'''
        self.name = name
        self.RGB = tuple([red, green, blue])
        self.color_difference = dict()
        self.closest_colour = None
colour_list = list()
for item in colors:
    (name, red, green, blue) = item.split(',')
    colour_list.append(colour(name, int(red), int(green), int(blue)))
all_colors = str()    
for (index, colour_item) in enumerat(colour_list):
    #Find 3D distances to all other colours
    closest = 1E7
    color_str = colour_item.name + '\t' + str(colour_item.RGB[0]) + '\t' +\
                                          str(colour_item.RGB[1]) + '\t' +\
                                          str(colour_item.RGB[2])
    #compare with other colurs only one, start with next colour
    color_str += '\t'*index
    index += 1
    for other_colour in colour_list[index:]:
        distance = ((colour_item.RGB[0] - other_colour.RGB[0])**2 + \
                    (colour_item.RGB[1] - other_colour.RGB[1])**2 + \
                    (colour_item.RGB[2] - other_colour.RGB[2])**2)**(1/2)
        colour_item.color_difference[other_colour.name] = distance
        if distance < closest:
            closest = distance
            colour_item.closest_colour = other_colour.name
        color_str += '\t' + str(distance)
    all_colors += color_str + '\n'

color_output = structures_path / 'ColorDistances.txt'
color_output.write_text(all_colors) 

