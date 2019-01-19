from StructureData import update_structure_references, load_structure_references
from WriteStructureTemplate import build_templates
from SelectTemplates import select_templates
from pathlib import Path


base_path = Path(r"C:\Users\gsalomon\OneDrive - Queen's University\Work\Structure Dictionary\Template Spreadsheets")

structures_lookup_file_name = 'Structure Lookup.xlsx'
structures_file_path = base_path / structures_lookup_file_name
#update_structure_references(structures_file_path, ref_file_name)

ref_file_name='StructureData.pkl'
structures_pickle_file_path = base_path / ref_file_name
structures_lookup = load_structure_references(structures_pickle_file_path)

templates = ['CE8-Brain', 'Brain Anatomy']
template_list = select_templates(base_path, templates)
structure_data = build_templates(template_list, base_path, structures_lookup, include_structure_list=False)

structures_file_name = base_path / 'Structure data.txt'
structure_data.to_csv(str(structures_file_name), sep=';', index=False)
