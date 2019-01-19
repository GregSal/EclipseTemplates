'''
Created on Sun Jan 13 2019
@author: gsalomon

Update list of structure templates.
'''
from pathlib import Path
from typing import Union, List, Dict, Tuple, Any
from collections import OrderedDict
import xlwings as xw
import pandas as pd

import utilities_path
from logging_tools import config_logger
from file_utilities import set_base_dir, get_file_mod_time
from spreadsheet_tools import open_book, load_definitions, append_data_sheet
from data_utilities import drop_empty_items

import Tables as tb
from StructureData import load_structure_references, build_structures_list
from StructureData import define_structure_attributes
from StructureData import update_structure_references


Data = pd.DataFrame
HeaderValue = Union[str, float, int]
HeaderData = Dict[str, HeaderValue]
LOGGER = config_logger(level='INFO')


def set_template_defaults()->HeaderData:
    '''Define the default values for all template header variables.
    Returns:
        A dictionary with all template header variables as keys and their
        defaults as values.
    '''
    template_defaults = {'Version': 1.1,
                         'TemplateType': 'Structure',
                         'TemplateID': 'Invalid',
                         'workbook_name': Path(r'.\Invalid.file'),
                         'sheet_name': 'Invalid',
                         'Modification Date': '',
                         'Columns': 3,
                         'Diagnosis': '',
                         'TreatmentSite': '.All',
                         'TemplateCategory': 'Generic',
                         'Status': 'Active',
                         'Template file name': 'Structure_template.xml',
                         'Author': ';',
                         'Description': '',
                         'ApprovalStatus': 'Unapproved',
                         'ApprovalHistory': '',
                         'LastModified': ''}
    return template_defaults


def set_template_selection(template_info: HeaderData)->HeaderData:
    '''Return a dictionary containing a subset of the template header data.
    Arguments:
        template_info {HeaderData} -- The dictionary containing the template
            header data.
    Returns:
        A dictionary containing the selected subset of the template header
        data to be stored in the template list spreadsheet.
    '''
    template_vars = ('TemplateID', 'TemplateCategory', 'TreatmentSite',
                     'workbook_name', 'sheet_name', 'Modification Date',
                     'Number_of_Structures', 'Description', 'Diagnosis',
                     'Author', 'Columns', 'Template file name', 'Status',
                     'TemplateType', 'ApprovalStatus')
    all_template_data = pd.DataFrame([template_info])
    template_selection = all_template_data.loc[:,template_vars]
    return template_selection


def set_structures_selection(structures: Data)->Data:
    '''Return a DataFrame containing the desired structure variables.
    Arguments:
        structures {Data} -- The DataFrame containing the structure data.
    Returns:
        A dictionary containing the selected subset of the structure data to
        be stored in the template list spreadsheet.
    '''
    structure_vars = ('StructureID', 'Name', 'Label', 'StructureCategory',
                      'VolumeType', 'StructureCode', 'CodeScheme',
                      'VolumeCode', 'ColorAndStyle', 'DVHLineWidth',
                      'DVHLineStyle', 'DVHLineColor', 'SearchCTLow',
                      'SearchCTHigh', 'TemplateID', 'TemplateType',
                      'Description', 'Diagnosis', 'TreatmentSite',
                      'TemplateCategory', 'Status', 'Template file name',
                      'Author', 'ApprovalStatus')
    structure_selection = structures.loc[:,structure_vars]
    return structure_selection


def find_template_files(template_directory: Path,
                        file_pattern='Templates.xlsx',
                        scan_subdir=False)->List[Path]:
    '''Scan a directory for template files.
    Attributes:
        template_directory {Path} -- the directory to scan for template files.
        file_pattern: {optional, str} -- The search pattern to use for the
            template files. Default='Templates.xlsx'
        scan_subdir {optional, bool} -- Whether to scan subdirectories of
            template_directory.  DefaultFalse.
    Returns:
        A list of all files in template_directory matching file_pattern.
    '''
    if scan_subdir:
        scan_pattern = '**/*' + file_pattern
    else:
        scan_pattern = '*' + file_pattern
    files = [file for file in template_directory.glob(scan_pattern)
             if '$' not in file.name]
    return files


def get_sheets(file: Path)->List[xw.Sheet]:
    '''Return a list of sheets for a given excel file.
    Attributes:
        file {Path} -- The path to an excel file.
    Returns:
        A list of all worksheets in the excel file.
    '''
    workbook = open_book(file)
    sheets = [sheet for sheet in workbook.sheets]
    return sheets


def read_template_header(data_sheet: xw.Sheet,
                         starting_cell='A3')->HeaderData:
    '''Load the header information for a structure template.
    The header data is assumed to form two columns where the first column is
    the attribute name and the matching second column is the attribute value.
    Attributes:
        data_sheet {xw.Sheet} -- The excel sheet containing the structure
            template.
        starting_cell {optional, str} the starting cell of the template
            header.  Default='A3'
    Returns:
        A dictionary, containing the template header attributes.
    '''
    template_defaults = set_template_defaults()
    table_info = load_definitions(data_sheet, starting_cell)
    table_info = drop_empty_items(table_info)
    table_definitions = template_defaults.copy()
    table_definitions.update(table_info)
    table_definitions['Columns'] = int(table_definitions['Columns'])
    return table_definitions


def define_structure_table(file_path: Path, sheet_name: str,
                           struc_columns: int)->tb.Table:
    '''Create Table definitions for the structure template.
    Arguments:
        file_path {Path} -- The path to the excel file containing the
            structure template.
        sheet_name {str} -- The name of the worksheet containing the
            structure template.
        struc_columns {int} -- The number of columns in the structure
            template.
    Returns:
        A table definition for the Structure Template.
    '''
    # FIXME move to StructureData and rename
    str_index = 'ID'
    struc_title = 'Template Structures'
    struc_offset = 'D1'
    structures_dfn = define_structure_attributes()
    structures_table = tb.Table(file_path, sheet_name, struc_title, str_index,
                                struc_offset, struc_columns,
                                variables=structures_dfn)
    return structures_table


def rebuild_structures_lookup(structures_file_path: Path,
                              structures_pickle_file_path: Path):
    '''Recreate the Structures lookup pickle file.
    Arguments:
        structures_file_path {Path} -- The path to the Structures definition
            spreadsheet.
        structures_pickle_file_path {Path} -- The location of the file to
        write the Structures pickle file.
    '''
    update_structure_references(structures_file_path,
                                structures_pickle_file_path)


def read_template_data(file: Path, sheet: str, table_info: Dict[str, Any],
                       structures_lookup: Data)->Data:
    '''Read the template and structure data.
    Arguments:
        file {Path} -- The path to the template spreadsheet.
        sheet {str} -- The name of the template worksheet.
        table_info {Dict[str, Any]} -- THe table header data.
        structures_lookup {Data} The DataFrame containing the lookup table
            for the structures.
    Returns:
        The template structures info as a DataFrame
    '''

    structures_table = define_structure_table(file, sheet.name,
                                              table_info['Columns'])
    structures = build_structures_list(structures_table,
                                       structures_lookup)
    for (key, value) in table_info.items():
        structures[key] = value
    structures['StructureID'] = structures.loc[:, 'ID']
    return structures


def add_template_info(template_data: Data, table_info: Dict[str, Any])->Data:
    '''Add the template header info to the template data collection.
    Arguments:
        template_data {Data} -- The collection of data for all templates.
        table_info {Dict[str, Any]} -- The template header data to be added.
    Returns:
        The updated template data.
    '''
    template_selection = set_template_selection(table_info)
    template_data = template_data.append(template_selection,
                                         ignore_index=True)
    return template_data


def add_structure_info(structure_data: Data, structures: Data)->Data:
    '''Add the structures data to the template data collection.
    Arguments:
        structure_data {Data} -- The collection of data for all structures.
        structures {Data} -- The structure data for the template to be added.
    Returns:
    The updated structure data.
    '''
    structure_selection = set_structures_selection(structures)
    structure_data = structure_data.append(structure_selection,
                                            ignore_index=True)
    return structure_data



def main():
    template_directory = set_base_dir(
            r'Work\Structure Dictionary\Template Spreadsheets')
    template_list_file = template_directory / 'Template List.xlsx'
    structures_file_path = template_directory / 'Structure Lookup.xlsx'
    structures_pickle_file_path = template_directory / 'StructureData.pkl'
    template_table_info = dict(file_name=template_list_file,
                               sheet_name='templates',
                               new_file=True, new_sheet=True, replace=True)
    structure_table_info = template_table_info.copy()
    structure_table_info['sheet_name'] = 'structures'

    # rebuild_structures_lookup(structures_file_path, structures_pickle_file_path)

    structures_lookup = load_structure_references(structures_pickle_file_path)
    open_book(structures_file_path)

    template_files = find_template_files(template_directory)
    LOGGER.debug('Found {} template files'.format(len(template_files)))

    template_data = pd.DataFrame()
    structure_data = pd.DataFrame()
    for file in template_files:
        LOGGER.debug('Scanning template file: {}'.format(file.name))
        file_mod_time = get_file_mod_time(file)
        workbook_sheets = get_sheets(file)
        LOGGER.debug('Found {} template worksheets'.format(
            len(workbook_sheets)))
        for sheet in workbook_sheets:
            template_info = read_template_header(data_sheet=sheet,
                                              starting_cell='A3')
            template_info['workbook_name'] = file.name
            template_info['sheet_name'] = sheet.name
            template_info['Modification Date'] = file_mod_time
            LOGGER.debug('Found template: {} in sheet: {}'.format(
                template_info['TemplateID'], sheet.name))
            structures = read_template_data(file, sheet, template_info,
                                            structures_lookup)
            num_structures = len(structures)
            template_info['Number_of_Structures'] = num_structures
            LOGGER.debug('Found {} structures'.format(num_structures))
            template_data = add_template_info(template_data, template_info)
            structure_data = add_structure_info(structure_data, structures)
        xw.books.active.close()
    append_data_sheet(template_data, **template_table_info)
    append_data_sheet(structure_data, **structure_table_info)


if __name__ == '__main__':
    main()
