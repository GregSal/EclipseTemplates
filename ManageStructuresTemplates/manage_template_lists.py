'''
Created on Sun Jan 13 2019
@author: gsalomon

Update list of structure templates.
'''
from pathlib import Path
from typing import Union, List, Dict, Any
from pickle import dump, load
import xlwings as xw
import pandas as pd

from file_utilities import get_file_path, get_file_mod_time
from spreadsheet_tools import open_book, load_definitions, append_data_sheet
from data_utilities import drop_empty_items

import Tables as tb
from StructureData import load_structure_references, build_structures_list
from StructureData import define_structure_attributes
from StructureData import update_structure_references
tb.VARIABLE_TYPES.append('Template_List')

Data = pd.DataFrame
DataLookup = Union[Data, Path]
PathInput = Union[Path, str]
HeaderValue = Union[str, float, int]
HeaderData = Dict[str, HeaderValue]


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
                         'modification_date': '',
                         'Columns': 3,
                         'Diagnosis': '',
                         'TreatmentSite': '.All',
                         'TemplateCategory': 'Generic',
                         'Status': 'Active',
                         'TemplateFileName': 'Structure_template.xml',
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
                     'workbook_name', 'sheet_name', 'modification_date',
                     'Number_of_Structures', 'Description', 'Diagnosis',
                     'Author', 'Columns', 'TemplateFileName', 'Status',
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
                      'TemplateCategory', 'Status', 'TemplateFileName',
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
        table_info {Dict[str, Any]} -- The table header data.
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


def scan_template_worksheet(file, sheet, file_mod_time, structures_lookup):
    template_info = read_template_header(data_sheet=sheet,
                                      starting_cell='A3')
    template_info['workbook_name'] = file.name
    template_info['sheet_name'] = sheet.name
    template_info['modification_date'] = file_mod_time
    structures = read_template_data(file, sheet, template_info,
                                    structures_lookup)
    num_structures = len(structures)
    template_info['Number_of_Structures'] = num_structures
    return structures, template_info


def scan_template_workbook(file, structure_data, structures_lookup, template_data):
    file_mod_time = get_file_mod_time(file)
    workbook_sheets = get_sheets(file)
    for sheet in workbook_sheets:
        structures, template_info = scan_template_worksheet(file, sheet, file_mod_time, structures_lookup)
        template_data = add_template_info(template_data, template_info)
        structure_data = add_structure_info(structure_data, structures)
    xw.books.active.close()
    return structure_data, template_data


def update_template_list(template_directory: Path, template_table_info: dict,
                         template_list_pickle_file_path: Path,
                         structure_table_info: dict,
                         structures_data: DataLookup,
                         structures_file_path: Path = None):
    if isinstance(structures_data, Data):
        structures_lookup = structures_data
    else:
        structures_lookup = load_structure_references(structures_data)
    if structures_file_path:
        open_book(structures_file_path)

    template_files = find_template_files(template_directory)
    template_data = pd.DataFrame()
    structure_data = pd.DataFrame()

    for file in template_files:
        structure_data, template_data = scan_template_workbook(file, structure_data, structures_lookup, template_data)
    append_data_sheet(template_data, **template_table_info)
    append_data_sheet(structure_data, **structure_table_info)
    file = open(str(template_list_pickle_file_path), 'wb')
    dump(template_data, file)
    file.close()


def define_template_list():
    '''Create a dictionary with Type Variable values that define the template list columns.
    '''
    var_type = 'Template_List'
    def is_int(x): return isinstance(x,int)
    def is_string(x): return isinstance(x,str)
    # TODO more attribute checks should be added to the attribute definitions
    # TODO make attribute checks more tolerant ie. if type conversion works

    template_def = [('workbook_name', is_string, 'Structure Templates.xlsx'), \
                     ('sheet_name', is_string, None), \
                     ('title', is_string, None), \
                     ('Columns', is_int, 3), \
                     ('TemplateFileName', is_string, 'template.xml'), \
                     ('Status', None, True)]
    return  {ID: tb.Variable(ID, var_type, validate=val, default=dflt)
                              for (ID, val, dflt) in template_def}


def load_template_references(pickle_file_name: PathInput,
                             sub_dir: str = None,
                             base_path: Path = None)->pd.DataFrame:
    template_pkl_path = get_file_path(pickle_file_name, sub_dir, base_path)
    file = open(str(template_pkl_path), 'rb')
    template_list = load(file)
    return template_list


def import_template_list(template_list_pickle_file_path: Path):
    '''Import the list of active templates.
    '''
    template_list = load_template_references(template_list_pickle_file_path)
    active_templates = template_list[template_list.Status == 'Active']
    active_templates['title'] = active_templates['TemplateID']
    active_templates.set_index('TemplateID', inplace=True)
    active_templates['Columns'] = active_templates['Columns'].astype('int64')
    return active_templates


def select_templates(template_list_path: Path, selections_list=None):
    '''build a list of templates from a list of template names.
    If selections is None, all active templates are used.
    '''
    column_selection = ['title', 'Columns', 'TemplateFileName',
                        'workbook_name', 'sheet_name']
    active_templates = import_template_list(template_list_path)
    if selections_list:
        selections = selections_list
    else:
        selections = ':'
    # FIXME Check for existence of templates in selections list
    selected_template_data = active_templates.loc[selections,column_selection]
    template_list = selected_template_data.to_dict(orient='record')
    return template_list


def main():
    base_dir = Path(r'\\dkphysicspv1\e$\Gregs_Work')
    template_directory = base_dir / r'\Eclipse\Template Management\External Beam Templates\Structure Templates\Template Spreadsheets'
    template_list_file = template_directory / 'Template List.xlsx'
    structures_file_path = template_directory / 'Structure Lookup.xlsx'
    structures_pickle_file_path = template_directory / 'StructureData.pkl'
    template_list_pickle_file_path = template_directory / 'TemplateData.pkl'
    template_table_info = dict(file_name=template_list_file,
                               sheet_name='templates',
                               new_file=True, new_sheet=True, replace=True)
    structure_table_info = template_table_info.copy()
    structure_table_info['sheet_name'] = 'structures'

    # rebuild_structures_lookup(structures_file_path, structures_pickle_file_path)

    update_template_list(template_directory, template_table_info,
                         template_list_pickle_file_path,
                         structure_table_info, structures_pickle_file_path,
                         structures_file_path)


if __name__ == '__main__':
    main()
