'''Define functions that can be called from Excel macros
'''
from pathlib import Path
from StructureData import load_structure_references
from WriteStructureTemplate import build_templates
from SelectTemplates import import_template_list, select_templates


base_path = Path(r"C:\Users\gsalomon\OneDrive - Queen's University\Work\Structure Dictionary\Template Spreadsheets")
# %% Load Structures reference
ref_file_name='StructureData.pkl'
structures_pickle_file_path = base_path / ref_file_name
structures_lookup = load_structure_references(structures_pickle_file_path)
active_templates = import_template_list(base_path)

templates = ['Prostate 2Ph VMAT', 'H&N VMAT', 'Lung VMAT']
template_list = active_templates.loc[templates,:].to_dict(orient='record')
#template_list = select_templates(base_path, templates)
#structure_data = build_templates(template_list, base_path, structures_lookup, include_structure_list=False)
