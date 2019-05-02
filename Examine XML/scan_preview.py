# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from pathlib import Path
# Set the path to the Utilities Package.
from __init__ import add_path
add_path('utilities_path')

from file_utilities import set_base_dir
from logging_tools import config_logger, file_logger
#logger = config_logger('DEBUG')
logger = file_logger('log_file.txt', 'INFO')


def get_str(file_text, search_str, begin_at=0):
    offset = len(search_str)
    found = file_text.find(search_str, begin_at)
    if found == -1:
        return '', None
    start = found + offset
    end = file_text.find('\n', start)
    return (file_text[start:end], end)


def get_line(file_text, begin_at):
    found = file_text.find('\n', begin_at)
    if found == -1:
        return '', None
    start = found + 1
    end = file_text.find('\n', start)
    return (file_text[start:end], end)


def get_objectives(file_text, index):
    data, index = get_line(file_text, index)
    while data:
        data, index = get_line(file_text, index)
        if index:
            objective_items = data.split(' ')
            yield '\t'.join(objective_items), index


def get_structure(file_text, template_id, index):    
    while index:
        structure_str = ''  
        logger.debug('Sturucture Str Before= %s' %structure_str)
        structure_id, index = get_str(file_text, 'Structure Objective: ', index)
        if index:            
            logger.debug('Sturucture = %s\tIndex = %d' %(structure_id, index))
            identifier_fields = '\t'.join([template_id, structure_id]) + '\t'
            index = get_str(file_text, 'Objectives', index)[1]
            if index:
                for objective_str, index in get_objectives(file_text, index):
                    if objective_str:
                        structure_str += identifier_fields + objective_str + '\n'
        logger.debug('Sturucture Str After= %s' %structure_str)
        yield structure_str, index
        
  
def main():
    base_dir = set_base_dir(r'Work\Structure Dictionary')
    template_preview_path_str = r'Template Archive\Objective Template Preview'
    preview_dir = base_dir / template_preview_path_str
    
    output_file = 'preview_data.csv'
    #output_path = base_dir / template_preview_path_str / output_file
    output_path = Path.cwd() / output_file

    save_str = ''
    for file_path in preview_dir.glob('*.txt'):
        file_text = file_path.read_text()
        template_id, index = get_str(file_text, 'Id: ')
        for structure_items, index in get_structure(file_text, template_id, index):
            if index:
                logger.debug('Sturucture Items = %s\t****Index = %d' %(structure_items, index))
                save_str += structure_items
    output_path.write_text(save_str)    
                
#file_name = 'IMRT CNS 40in15.txt'
#file_path = base_dir / template_preview_path_str / file_name
# file_path = Path.cwd()  / file_name
# output_path = Path.cwd()  / output_file

if __name__ == '__main__':
    main()
    