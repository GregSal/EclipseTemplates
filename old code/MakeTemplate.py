def make_template(template_data, structures):
    '''Create a template xml from template and structure data.
    '''
    template = ET.Element('StructureTemplate',attrib={'Version':'1.0', 
                'xmlns:xsi':"http://www.w3.org/2001/XMLSchema-instance"})
    #template = ET.Element('StructureTemplate',attrib={'Version':'1.1', 
    #            'xmlns:xsi':"http://www.w3.org/2001/XMLSchema-instance"})
    add_preview(template, template_data)
    structure_set = ET.SubElement(template, 'Structures')
    for structure_data in structures:
        add_structure(structure_set, structure_data)
    template_tree = ET.ElementTree(template)
    return template_tree

def store_data(keys, data_list):
    '''Pack items from a coma delimited data string into a dict using the values in the first line as keys.
    All lines must have the same number of variables.
    '''
    data_dict = dict()
    for (key, data) in zip(keys, data_list.split(',')):
        data_dict[key] = data.strip()
    return data_dict
