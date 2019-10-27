#importing xml & json libraries
import xml.etree.ElementTree as ET
import json as JSON

root = None
path = ""
all_colors_dec = []
all_colors_hex = []
all_color_names = []

# getting the theme name from filename (silly, I know)
def get_theme_name(path):
    path = str(path)
    last_slash_index = path.rfind("/")
    filename_wext = path[last_slash_index + 1:]
    ext_dot_index = filename_wext.rfind(".itermcolors")
    theme_name = filename_wext[:ext_dot_index].lower()
    return theme_name

# as our .itermcolors is two levels xml, we get to the root of 2nd one
def get_inner_tree(path):
    tree = ET.parse(path)
    pre_root = tree.getroot()
    root = pre_root[0]
    return root

# getting color values from fractionals in .itermcolors
def get_color_values(root):
    for node in root.findall('dict'):
        color_values = []
        for color in node.findall('real'):
            color_value = int(float(color.text)*255)
            color_values.append(color_value)
            bgr_to_rgb = color_values[::-1]
        all_colors_dec.append(bgr_to_rgb)

# getting color names from .itermcolors
def get_color_names(root):
    for color_type in root.findall('key'):
        all_color_names.append(color_type.text)

# converting dec colors to hex values in common notation
def convert_colors(all_colors_dec):
    for value_list in all_colors_dec:
        color_string = ''
        for value in value_list:
            color_string += str(hex(value))[2::]
        all_colors_hex.append("#" + color_string)

# combining results with names and colors into one dict
def combine_results(all_color_names, all_colors_hex):
    return dict(zip(all_color_names, all_colors_hex))

# getting theme type based on it's (somewhat subjective) "lightness"
def get_theme_type(dictionary):
    # color = dictionary.get("Background Color")
    color_grades = []
    sublist = all_colors_dec[16]
    for value in sublist[:3]:
        if value > 150:
            color_grades.append(True)   
        else:
            color_grades.append(False)
    if color_grades.count(True) > 1:
        return "light"
    else:
        return "dark"

# just dumping known values together with common VSCode ones
def get_colors_dict(dictionary):
    colors_dict = {
        "editor.BackgroundColor" : dictionary.get("Background Color"),
        "editor.ForegroundColor" : dictionary.get("Foreground Color")
        }
    colors_dict_updated = {**colors_dict, **dictionary}
    return colors_dict_updated

# forming the structure of our json
def form_scaffolding(dict_):
    scaffolding_dict = {
        "name" : get_theme_name(path),
        "type" : get_theme_type(dict_),
        "colors" : get_colors_dict(dict_)
        }
    return scaffolding_dict

# and now for the tricky part
root = get_inner_tree('bluloco_light_iterm/BlulocoLight.itermcolors')
path = 'bluloco_light_iterm/BlulocoLight.itermcolors'
get_color_values(root)
get_color_names(root)
convert_colors(all_colors_dec)

file = open("test1.json", "w+")
dict_ = combine_results(all_color_names, all_colors_hex)
theme_type = get_theme_type(dict_)
theme_name = get_theme_name(path)
dict_ = form_scaffolding(dict_)
JSON.dump(dict_, file, indent=4)
file.close()

print(get_theme_name('bluloco_light_iterm/BlulocoLight.itermcolors'))
print(combine_results(all_color_names, all_colors_hex))
