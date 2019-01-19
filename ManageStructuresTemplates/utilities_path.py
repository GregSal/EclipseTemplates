'''
Created on Mon Jan 10 2019

@author: Greg Salomons
Set the path to the Utilities Package.
'''
from pathlib import Path
import sys
# utilities_path = r"C:\Users\Greg\OneDrive - Queen's University\Python\Projects\Utilities"

utilities_path = Path.cwd() / '..\\..\\..\\Utilities'
utilities_path_str = str(utilities_path.resolve())
sys.path.append(utilities_path_str)
