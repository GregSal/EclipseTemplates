'''
Manage Structure Templates
@author: Greg Salomons
'''
from pathlib import Path
import sys

def add_path(relative_path: str):
    # Set the path to the Utilities Package.
    relative_paths = dict(
        utilities_path = r'..\..\..\Utilities',
        variable_path = r'..\..\..\Utilities\CustomVariableSet',
        templates_path = r'..\ManageStructuresTemplates'
        )
    new_path = Path.cwd() / relative_paths[relative_path]
    new_path_str = str(new_path.resolve())
    sys.path.append(new_path_str)



add_path('utilities_path')
add_path('variable_path')
add_path('templates_path')
