'''
Created on Wed Mar 13 2019
@author: Greg Salomons

Basic function calls to update reference data and generate XML templates.
'''

from logging_tools import config_logger
from pathlib import Path
import pandas as pd
from file_utilities import set_base_dir, PathInput
from data_utilities import select_data
from spreadsheet_tools import open_book
from StructureData import update_structure_references
from StructureData import load_structure_references
from manage_template_lists import update_template_list
from manage_template_lists import select_templates
from manage_template_lists import load_template_references
from WriteStructureTemplate import build_templates

LOGGER = config_logger(level='DEBUG')

#
# Function calls
#
def rebuild_structures():
    '''Update the structures pickle file from the Structure Lookup spreadsheet.
    '''
    update_structure_references(structures_file_path,
                                structures_pickle_file_path)


def update_template_data(template_directory: Path,
                         template_list_file: Path,
                         template_list_pickle_file_path: Path,
                         structures_file_path: Path,
                         structures_pickle_file_path: Path):
    '''Update the templates list spreadsheet and the corresponding pickle file.
    '''
    template_table_info = dict(file_name=template_list_file,
                               sheet_name='templates',
                               new_file=True, new_sheet=True, replace=True)
    structure_table_info = template_table_info.copy()
    structure_table_info['sheet_name'] = 'structures'
    structures_lookup = load_structure_references(structures_pickle_file_path)
    update_template_list(template_directory, template_table_info,
                         template_list_pickle_file_path,
                         structure_table_info, structures_lookup)


def load_template_data(pickle_file_name: PathInput,
                       sub_dir: str = None,
                       base_path: Path = None)->pd.DataFrame:
    '''Load the templates list from the pickle file.
    '''
    return load_template_references(pickle_file_name, sub_dir, base_path)


######################
def build_xml(selected_templates, template_directory, xml_directory,
              structures_pickle_file_path, template_list_pickle_file_path):
    structures_lookup = load_structure_references(structures_pickle_file_path)
    template_list = select_templates(template_list_pickle_file_path,
                                     selected_templates)
    build_templates(template_list, template_directory, xml_directory,
                    structures_lookup)


###################
# Stepwise updates
##################
#%%

if __name__ == '__main__':
    #
    # File and Template Settings
    #
    template_directory = set_base_dir(
            r'Work\Structure Dictionary\Template Spreadsheets')
    xml_directory = set_base_dir(
            r'Work\Structure Dictionary\Template XML Files')
    template_list_file = template_directory / 'Template List.xlsx'
    template_list_pickle_file_path = template_directory / 'TemplateData.pkl'
    structures_file_path = template_directory / 'Structure Lookup.xlsx'
    structures_pickle_file_path = template_directory / 'StructureData.pkl'
    template_table_info = dict(file_name=template_list_file,
                                sheet_name='templates',
                                new_file=True, new_sheet=True, replace=True)
    structure_table_info = template_table_info.copy()
    structure_table_info['sheet_name'] = 'structures'
    selected_templates = ['Lung SBRT', 'FSRT', 'Breast']

    # Action
    #rebuild_structures()

    #structures_lookup = load_structure_references(structures_pickle_file_path)
    #open_book(structures_file_path)
    #update_template_data()

    build_xml()
