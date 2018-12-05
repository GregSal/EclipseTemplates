from pathlib import Path
import xlwings as xw

#test_path = Path(r"C:\Users\gsalomon\OneDrive for Business\Structure Dictionary\Python code\Structures\Structures")
test_path = Path(r"C:\Users\Greg\OneDrive - Queen's University\Structure Dictionary\Python code\Structures\Structures")

STRUCTURE_HEADING = 'Structure'
template_lookup = 'Template Lookup.xlsx'
selected_template = 'H&N 70 in 35'

template_book = xw.Book(template_lookup)
sheet_names = {sht.name:index for (index, sht) in enumerate(template_book.sheets)}
template_sheet = sheet_names[selected_template]

structure_lookup = dict() # Replace with call to generate lookup

#Load Template Header
active_sheet = template_book.sheets[template_sheet]
template_range = active_sheet.range('A1').expand('table')
template_dict = {data[0]:data[1] for data in template_range.value}
offset = template_range.shape[0]+1
structure_range = template_range.offset(row_offset=offset).expand()
structure_data = structure_range.value
headers = structure_data.pop(0)
structures_list = list()
for str_data in structure_data:
    structure_dict = {key:value for (key, value) in zip(headers, str_data)}
    structure = structure_dict.pop(STRUCTURE_HEADING)
    #data = structure_lookup.get(structure)
    #if data is None:
    #    pass #Replace with raise missing structure error
    #else:
    #    structure_dict.update(structure_data)
    structures_list.append(structure_dict)
structures_list

