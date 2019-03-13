'''
Created on Wed Mar 13 2019
@author: Greg Salomons

Basic function calls to update reference data and generate XML templates.
'''

from pathlib import Path
import pandas as pd
import xlwings as xw
from logging_tools import config_logger
from file_utilities import set_base_dir, get_file_mod_time
from StructureData import load_structure_references, build_structures_list
from SelectTemplates import select_templates
from WriteStructureTemplate import make_template
from WriteStructureTemplate import build_template_data, define_template_tables
from update_template_list import rebuild_structures_lookup, find_template_files
from update_template_list import scan_template_worksheet, get_sheets
from update_template_list import add_template_info, add_structure_info
from spreadsheet_tools import append_data_sheet, open_book
LOGGER = config_logger(level='DEBUG')

#
# Function calls
#
def rebuild_structures():
    '''Update the structures pickle file from the Structure Lookup spreadsheet.
    '''
    rebuild_structures_lookup(structures_file_path,
                              structures_pickle_file_path)

def update_template_data():
    update_template_list(template_directory, structures_lookup,
                         structure_table_info, template_table_info)

######################
def build_xml():
    selected_templates = ['CE8-Brain', 'Brain Anatomy']
    structures_lookup = load_structure_references(structures_pickle_file_path)
    template_list = select_templates(template_list_file, templates)
    build_templates(template_list, template_directory, structures_lookup)


###################
# Stepwise updates
##################
def scan_template_workbook(file, structures_lookup,
                           structure_data, template_data):
    LOGGER.debug('Scanning template file: {}'.format(file.name))
    file_mod_time = get_file_mod_time(file)
    workbook_sheets = get_sheets(file)
    LOGGER.debug('Found {} template worksheets'.format(len(workbook_sheets)))

    for sheet in workbook_sheets:
        structures, template_info = scan_template_worksheet(
            file, sheet, file_mod_time, structures_lookup)
        template_data = add_template_info(template_data, template_info)
        structure_data = add_structure_info(structure_data, structures)
    xw.books.active.close()
    return structure_data, template_data

def update_template_list(template_directory: Path, structures_lookup: Path,
                         structure_table_info: dict, template_table_info: dict):
    template_files = find_template_files(template_directory)
    LOGGER.debug('Found {} template files'.format(len(template_files)))

    template_data = pd.DataFrame()
    structure_data = pd.DataFrame()

    for file in template_files:
        structure_data, template_data = scan_template_workbook(
            file, structures_lookup, structure_data, template_data)
    append_data_sheet(template_data, **template_table_info)
    append_data_sheet(structure_data, **structure_table_info)

def build_templates(template_list, template_directory, output_path, structures_lookup):
    '''Build a collection of structure template files from the list of templates
    in template_list that describe template data in the template file. Structure
    data used for the templates comes from the structures_lookup data-frame.
    '''
    for tmpl in  template_list:
        LOGGER.debug('Building Template: %s' %tmpl['title'])
        template_save_file = output_path / tmpl['output_file_name']
        template_file_path = template_directory / tmpl['workbook_name']
        (template_table, structures_table) = define_template_tables(
            template_file_path, sheet_name=tmpl['sheet_name'],
            tmpl_title= tmpl['title'], struc_columns=tmpl['columns'])
        #Load the template and structure data from the excel worksheet
        template_data = build_template_data(template_table)
        structures = build_structures_list(structures_table, structures_lookup)
        # convert the template and structure data to an XML file
        template_tree = make_template(template_data, structures, template_save_file)


if __name__ == '__main__':
    #
    # File and Template Settings
    #
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

    # Action
    #rebuild_structures()

    structures_lookup = load_structure_references(structures_pickle_file_path)
    open_book(structures_file_path)
    update_template_data()

    selected_templates = ['CE8-Brain', 'Brain Anatomy']
