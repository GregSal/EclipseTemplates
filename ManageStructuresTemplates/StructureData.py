''' Functions to load a structure lookup table from a set of tables in an excel file.
Structure Attributes are defined, Structure Tables are defined, The tables are read in, checked and defaults filled in.
    Functions:
        define_structure_attributes
        define_structure_tables
        read_structure_tables

'''

from typing import Union
from pathlib import Path
from pickle import dump, load
import re
import pandas as pd
import xml.etree.ElementTree as ET

import Tables as tb

PathInput = Union[Path, str]

#import LoggingConfig as log
#logger = log.logging_init(__name__)

tb.VARIABLE_TYPES = ['Structure', 'Template']

def define_structure_attributes():
    '''Create a dictionary with Type Variable values that define all of the structure attributes.
    The attributes:
        EUDAlpha
        TCPAlpha
        TCPBeta and
        TCPGamma
        Are supplied but not used,
        the add_structure method forces them to be: 'xsi:nil="true"'
    '''
    var_type = 'Structure'
    is_string = lambda x: isinstance(x,str)
    id_check = lambda x: is_string(x) and len(x) < 13
    # TODO Merge with define_structure_table from update_template_list
    # TODO more attribute checks should be added to the attribute definitions

    structure_def = [('StructureID', id_check, None), \
                     ('Name', is_string, ''), \
                     ('StructureCategory', is_string, ''), \
                     ('VolumeID', None, ''), \
                     ('VolumeType', is_string, ''), \
                     ('VolumeCode', is_string, ''), \
                     ('VolumeCodeTable', is_string, ''), \
                     ('Label', is_string, None), \
                     ('StructureCode', None, None), \
                     ('CodeScheme', is_string, None), \
                     ('CodeSchemeVersion', None, None), \
                     ('TypeIndex', None, 2), \
                     ('ColorAndStyle', is_string, 'Blue'), \
                     ('SearchCTLow', None, 'Missing'), \
                     ('SearchCTHigh', None, 'Missing'), \
                     ('DVHLineColor', None, -16777216), \
                     ('DVHLineWidth', None, 1), \
                     ('DVHLineStyle', None, 0), \
                     ('EUDAlpha', None, 'xsi:nil="true"'), \
                     ('TCPAlpha', None, 'xsi:nil="true"'), \
                     ('TCPBeta', None, 'xsi:nil="true"'), \
                     ('TCPGamma', None, 'xsi:nil="true"')]
    return  {ID: tb.Variable(ID, var_type, validate=val, default=dflt)
                              for (ID, val, dflt) in structure_def}

def define_structure_lookup_tables(file_path: Path, structures: list):
    '''Create a list of Type Table values that define all of the structure
    tables required to build a complete structures data lookup.
    '''
    # Define the tables
    tables_def = [
         ['Structure Dictionary Assignment', 'Structure Dictionary', 6],
         ['Volume Types', 'Volume Type', 3],
         ['Structure colors', 'Structure Colors', 6],
         ['CT Search', 'HU Values', 3],
         ['DVH Lines', 'DVH',4]]
    # values for all tables
    offset = 'A1'
    index = 'Structure'
    # Rows is not yet implemented not using
    table_list = [tb.Table(file_path, sheet_name=sheet_name, title=title, \
                        index=index, offset=offset, columns=columns, \
                        variables=structures)
                  for (sheet_name, title, columns) in tables_def]
    return  table_list

def build_structures_lookup(structures_file_path: Path):
    structure_attributes = define_structure_attributes()
    structures_table_list = define_structure_lookup_tables(
        structures_file_path, structure_attributes)
    structures_lookup = tb.merge_tables(structures_file_path, \
                                        structures_table_list, \
                                        structure_attributes)
    structure_attributes = tb.process_defaults(structures_lookup, \
                                               structure_attributes)
    structures_lookup = tb.insert_defaults(structures_lookup, \
                                           structure_attributes)
    structures_lookup = tb.insert_missing_variables(structures_lookup, \
                                                    structure_attributes)
    return structures_lookup

def build_structures_list(structures_table, structures_lookup):
    '''Read in a list of structures and attributes.  Merge this with structures_lookup to generate a new DataFrame containing only the selected structures.
    '''
    template_structures = structures_table.read_table()
    #indexed_structures = template_structures.reset_index().set_index('Structure')
    merged_structures = template_structures.join(structures_lookup, on='Structure', rsuffix='_r')
    overlap = list(set(structures_lookup.columns) & set(template_structures.columns))
    for col in overlap:
        col_new = col+'_r'
        find_missing = template_structures[col].isnull()
        merged_structures.loc[find_missing,col] = merged_structures.loc[find_missing,col_new]
    #a.loc[b.loc[:,c[0]],c[0]] = a.loc[b.loc[:,c[0]],d[0]]

    #TODO Select and validate attributes in this table
    #selected_str = list(set(structures_lookup.index) & set(indexed_structures.index))
    #merged_structures = indexed_structures.combine_first(structures_lookup.loc[selected_str])
    #selected_structures = merged_structures.loc[selected_str]
    structures = merged_structures.reset_index()
    return structures

def build_structures_element(structures, version=10.0):
    '''Build an XML structures element with SubElements from the
    structures DataFrame using the structure data in structures_lookup.
    '''
    structure_set = ET.Element('Structures')
    for structure in structures.index:
        structure_data = dict(structures.loc[structure])
        add_structure(structure_set, structure_data, version)
    return structure_set

def add_structure(template, structure_data, version):
    '''Add a new structure to the template tree using the data in structure_data.
    The order of the elements is important
    The attributes:
        EUDAlpha
        TCPAlpha
        TCPBeta and
        TCPGamma
    Are forced to be: 'xsi:nil="true"'
    '''
    name = tb.get_value(structure_data, 'Name')
    new_structure = ET.SubElement(template, 'Structure', \
        attrib={'ID':structure_data['ID'], 'Name':name})
    structure_id = ET.SubElement(new_structure, 'Identification')

    volume_id = ET.SubElement(structure_id, 'VolumeID')
    volume_id.text = tb.get_value(structure_data, 'VolumeID')
    volume_code = ET.SubElement(structure_id, 'VolumeCode')
    volume_code.text = tb.get_value(structure_data, 'VolumeCode')
    volume_type = ET.SubElement(structure_id, 'VolumeType')
    volume_type.text = tb.get_value(structure_data, 'VolumeType')
    volume_code_table = ET.SubElement(structure_id, 'VolumeCodeTable')
    volume_code_table.text = tb.get_value(structure_data, 'VolumeCodeTable')

    if version == 13.6:
        code = tb.get_value(structure_data, 'StructureCode')
        scheme = tb.get_value(structure_data, 'CodeScheme')
        version = tb.get_value(structure_data, 'CodeSchemeVersion')
        structure_code = ET.SubElement(structure_id, 'StructureCode', \
            attrib={'Code':code, 'CodeScheme':scheme, 'CodeSchemeVersion':version})

    type_index = ET.SubElement(new_structure, 'TypeIndex')
    type_index.text = tb.get_value(structure_data, 'TypeIndex')

    color_and_style = ET.SubElement(new_structure, 'ColorAndStyle', )
    color_and_style.text = tb.get_value(structure_data, 'ColorAndStyle')

    # if SearchCT values are not given set a nil attribute
    SearchCTLow_value = tb.get_value(structure_data, 'SearchCTLow')
    if SearchCTLow_value == 'Missing':
        SearchCTLow = ET.SubElement(new_structure, 'SearchCTLow', attrib={'xsi:nil':"true"})
    else:
        SearchCTLow = ET.SubElement(new_structure, 'SearchCTLow')
        SearchCTLow.text = SearchCTLow_value

    SearchCTHigh_value = tb.get_value(structure_data, 'SearchCTHigh')
    if SearchCTHigh_value == 'Missing':
        SearchCTHigh = ET.SubElement(new_structure, 'SearchCTHigh', attrib={'xsi:nil':"true"})
    else:
        SearchCTHigh = ET.SubElement(new_structure, 'SearchCTHigh')
        SearchCTHigh.text = SearchCTHigh_value

    DVHLineStyle = ET.SubElement(new_structure, 'DVHLineStyle', )
    DVHLineStyle.text = tb.get_value(structure_data, 'DVHLineStyle')
    DVHLineColor = ET.SubElement(new_structure, 'DVHLineColor', )
    DVHLineColor.text = tb.get_value(structure_data, 'DVHLineColor')
    DVHLineWidth = ET.SubElement(new_structure, 'DVHLineWidth', )
    DVHLineWidth.text = tb.get_value(structure_data, 'DVHLineWidth')

    #Currently not used so always set as Nil
    EUDAlpha = ET.SubElement(new_structure, 'EUDAlpha', attrib={'xsi:nil':"true"})
    TCPAlpha = ET.SubElement(new_structure, 'TCPAlpha', attrib={'xsi:nil':"true"})
    TCPBeta = ET.SubElement(new_structure, 'TCPBeta', attrib={'xsi:nil':"true"})
    TCPGamma = ET.SubElement(new_structure, 'TCPGamma', attrib={'xsi:nil':"true"})

    return new_structure

def update_structure_references(structures_file_path: Path,
                                ref_file_name='StructureData.pkl')->Path:
    '''Recreate the Structures lookup pickle file.
    Arguments:
        structures_file_path {Path} -- The path to the Structures definition
            spreadsheet.
        structures_pickle_file_name {PathInput} -- The location of the file to
        write the Structures pickle file.
    Returns:
        The path to the new structures pickle file
    '''
    structures_lookup = build_structures_lookup(structures_file_path)
    if isinstance(ref_file_name, Path):
        structures_pickle_file_path = ref_file_name.resolve()
    else:
        base_path = structures_file_path.parent
        structures_pickle_file_path = base_path / ref_file_name
    file = open(str(structures_pickle_file_path), 'wb')
    dump(structures_lookup, file)
    file.close()
    return structures_pickle_file_path

def load_structure_references(structures_pickle_file_path)->pd.DataFrame:
    file = open(str(structures_pickle_file_path), 'rb')
    structures_lookup = load(file)
    return structures_lookup

if __name__ == '__main__':
    structures_file_path = Path(r'.\Template Tests.xlsx')
    structures_lookup = build_structures_lookup(structures_file_path)
    #print(structures_lookup)

    file_path = file_path = Path(r'.\Template Tests.xlsx')
    sheet_name = 'Test Template'
    title = 'Structures'
    offset = 'A6'
    index = 'ID'
    columns = 5
    structures_table = tb.Table(file_path, sheet_name, title, index, offset, columns, define_structure_attributes())
    structures = build_structures_list(structures_table, structures_lookup)
    print(structures)
    structure_set = build_structures_element(structures)

    #title = 'Test Template'
    #offset = 'A1'
    #columns = 8
    #template_table = tb.Table(file_path, sheet_name, title, offset=offset, columns=columns)
