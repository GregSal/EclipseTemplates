# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 11:35:35 2017

@author: gsalomon
"""
TEMPLATE_LIST_FILE = 'Template List.xlsx'

from pathlib import Path
import Tables as tb
from WriteStructureTemplate import build_templates
tb.VARIABLE_TYPES.append('Template_List')


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
                     ('columns', is_int, 3), \
                     ('output_file_name', is_string, 'template.xml'), \
                     ('in_use', None, True)]
    return  {ID: tb.Variable(ID, var_type, validate=val, default=dflt)
                              for (ID, val, dflt) in template_def}

def import_template_list(template_list_path: Path):
    '''Import the list of active templates.
    '''
    variables=define_template_list()
    template_list_table = tb.Table(template_list_path, 'templates', variables=variables)
    template_list = template_list_table.read_table()
    active_templates = template_list[template_list.in_use == 'True']
    active_templates['name'] = active_templates['title']
    active_templates.set_index('name', inplace=True)
    active_templates['columns'] = active_templates['columns'].astype('int64')
    return active_templates

def select_templates(template_list_path: Path, selections_list=None):
    '''build a list of templates from a list of template names.
    If selections is None, all active templates are used.
    '''
    active_templates = import_template_list(template_list_path)
    if selections_list is None:
        template_list = active_templates.to_dict(orient='record')
    else:
        # FIXME Check for existence of templates in selections list
        template_list = active_templates.loc[selections_list,:].to_dict(orient='record')
    return template_list


def main():
    base_path = Path(r'C:\Users\gsalomon\OneDrive for Business 1\Structure Dictionary')
    template_list_path = base_path / TEMPLATE_LIST_FILE
    template_list = select_templates(template_list_path, ['Gyne VMAT',r'H&N 70/35'])

    structures_lookup_file_name = 'Structure Lookup.xlsx'
    structures_file_path = base_path / structures_lookup_file_name
    structures_lookup = build_structures_lookup(structures_file_path)

    build_templates(template_list, base_path, structures_lookup, include_structure_list=False)

if __name__ == '__main__':
    main()