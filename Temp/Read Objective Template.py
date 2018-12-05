from pathlib import Path
import xml.etree.ElementTree as ET
import xlwings as xw
import pandas as pd

def display_element(element_item,indent=''):
    '''Return a string describing an XML element and its sum-elements.
    '''
    element_string = ''
    try:
        element_string += '{}Element:\t{}'.format(indent,element_item.tag) + '\n'
        attr = element_item.attrib
        if len(attr) > 0:
            element_string += '{}\tAttributes:'.format(indent) + '\n'
            for (key,item) in attr.items():
                element_string += '{}\t\t{:>20}:\t{:<30}'.format(indent,key,item) + '\n'
        text = element_item.text
        if text is not None:
           element_string += '{}\tValue:\t{}'.format(indent,text) + '\n'
        tail = element_item.tail
        if tail is not None:
           element_string += '{}\tTail:\t{}'.format(indent,tail) + '\n'
        if len(list(element_item)) > 0:
            element_string += '{}\tSub Elements:'.format(indent) + '\n'
            for sub_element in element_item: 
                element_string += display_element(sub_element,indent+'\t\t') + '\n'
    except AttributeError:
        pass
    return element_string

class Structure():
    '''Defines attributes for objective structures
    '''
    def __init__(self, struct):
        self.name = struct.get('ID')
        self.element = struct

    def get_color(self, struct=None):
        if struct is None:
            struct = self.element
        color = int(struct.find('Color').text)
        color_data = dict(red=color % 256, green=(color % (256*256)) // 256, blue=color // (256*256))
        color_data['color'] = color
        color_data['Structure ID'] = self.name
        return color_data

    def get_props(self, struct=None):
        if struct is None:
            struct = self.element
        struct_props = struct.find('StructureTarget')
        self.props = {prop.tag: prop.text for prop in struct_props}
        self.props['SurfaceOnly'] = struct.attrib.get('SurfaceOnly')
        self.props['Distance'] = struct.find('Distance').text
        self.props['SamplePoints'] = struct.find('SamplePoints').text
        self.props['SamplePoints'] = list(struct.find('SamplePoints').attrib)[0]
        return self.props

    def get_objectives(self, struct=None):
        if struct is None:
            struct = self.element
        objective_set = struct.find('StructureObjectives')
        objectives = objective_set.findall('Objective')
        if len(objectives) > 0:
            objective_list = [{item.tag: item.text
                         for item in obj}
                         for obj in objectives]
            for obj in objective_list:
                obj['ID'] = self.name
        else:
            objective_list = None
        self.objectives = objective_list
        return objective_list


def main():
    #base_path = Path(r"C:\Users\Greg\OneDrive - Queen's University\Structure Dictionary")
    base_path = Path(r"C:\Users\gsalomon\OneDrive for Business 1\Structure Dictionary")
    test_path = base_path / r'Python code\Structures\Objective Templates'
    #test_path = base_path
    #objective_template_file = 'TEST GS.xml'
    objective_template_file = 'IMRT H&N 70 in 35.xml'
    test_template_path = test_path / objective_template_file
    excel_file = test_template_path.with_suffix('.xlsx') 
    template_xls = xw.Book()
    template_xls.save(str(excel_file))

    tree = ET.parse(str(test_template_path))
    root = tree.getroot()

    template = root.find('Preview')
    template_ID = template.get('ID')
    print('Template:\t%s' %template_ID)
    sht = template_xls.sheets[0]
    sht.name = 'header'
    sht.range('A1').value = template.attrib
    sht.autofit('c')

    #TODO Add Type
    gen_opt = root.find('Helios')
    gen_opt_str = display_element(gen_opt)

    sht2 = template_xls.sheets.add('gen_opt')
    gen_opt_list = [line.split('\t') for line in gen_opt_str.split('\n')]
    gen_opt_tbl = pd.DataFrame(gen_opt_list)
    sht2.range('A1').value = gen_opt_tbl
    sht2.autofit('c')

    structure_set = root.find('ObjectivesAllStructures')
    structures = structure_set.findall('ObjectivesOneStructure')
    structures_list = [Structure(struct) for struct in structures]


    objective_list = []
    data_list = []
    for struct in structures_list:
        objectives = struct.get_objectives()
        if objectives is not None:
            objective_list.extend(struct.get_objectives())
        struct_data = struct.get_color()
        struct_data.update(struct.get_props())
        data_list.append(struct_data)
    structure_data = pd.DataFrame(data_list)

    sht4 = template_xls.sheets.add('objective data')
    sht4.range('A1').value = pd.DataFrame(objective_list)
    sht4.autofit('c')
    sht5 = template_xls.sheets.add('Structure data')
    sht5.range('A1').value = structure_data
    sht5.autofit('c')

    sht3 = template_xls.sheets.add('structures')
    sht3.range('A1').value = structure_data[['Structure ID', 'VolumeType', 'color']]
    sht3.autofit('c')
    template_xls.save(str(excel_file))


    #sht2.range('A1').options(transpose=True).value = gen_opt_str.split('\n')
    #struct_data = [(struct.get('ID'),  int(struct.find('Color').text)) for struct in structures]
    #print('\n'.join(struct_names)) 
    #sht2.range('A1').value = struct_data
    #struct_props = struct.find('StructureTarget')
    #props = [(prop.tag, prop.text) 
    #             for prop in struct_props]
    #print('\n'.join('\t%s:\t%s' % item
    #                  for item in props))
    #color = int(struct.find('Color').text)
    #rgb = (color % 256, 
    #       (color % (256*256)) // 256, 
    #       color // (256*256)) 
    #print('Color:\t{}\t{}'.format(color,rgb))
    #display_element(struct_props,'')
    #objective_set = struct.find('StructureObjectives')
    #objectives = objective_set.findall('Objective')
    #objective = [(item.tag, item.text) 
    #             for obj in objectives
    #             for item in obj]
    #if len(objective) > 0:
    #    print('\n'.join('\t%s:\t%s' % item 
    #                    for item in objective))
    
            
    #template_xls = xw.Book()
    #sht = template_xls.sheets[0]
    #sht.name = 'header'
    #sht.range('A1').value = template.attrib
    #sht.autofit('c')
    #template_xls.save(str(excel_file))
    #xw.view(template.attrib, sheet=None)
    #template_xls = xw.Book(str(excel_file))
    #sht = template_xls.sheets['header']
    #sht.range('A1').value = 'Foo 1'
    #general.set('ID','New Prescription')
    #new_file = new_templates / 'New Prescription.xml'
    #tree.write(str(new_file))
    #display_element(root,'')

main()


