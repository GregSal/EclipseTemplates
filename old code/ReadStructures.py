from pathlib import Path
import xlwings as xw

#test_path = Path(r"C:\Users\gsalomon\OneDrive for Business\Structure Dictionary\Python code\Structures\Structures")
test_path = Path(r"C:\Users\Greg\OneDrive - Queen's University\Structure Dictionary\Python code\Structures\Structures")
#test_spreadsheet = 'Export Test.xlsx'

STRUCTURE_TABLES = ['Structure Categories', \
                    'Structure Dictionary Assignment', \
                    'Volume Types', \
                    'Structure colors', \
                    'CT Searching', \
                    'DVH Lines']
STRUCTURE_HEADING = 'Structure'
structure_lookup = dict()
table_lookup = 'Structure Lookup.xlsx'
test_book = xw.Book(table_lookup)
sheet_names = {sht.name:index for (index, sht) in enumerate(test_book.sheets)}
sheets = [sheet_names[sht] for sht in STRUCTURE_TABLES]

for sheet_index in sheets:
    active_sheet = test_book.sheets[sheet_index]
    active_sheet.name
    rng1 = active_sheet.range('A1').expand('table')
    data = rng1.value
    headers = data.pop(0)
    for str_data in data:
        str_dict = {key:value for (key, value) in zip(headers, str_data)}
        structure = str_dict.pop(STRUCTURE_HEADING)
        structure_data = structure_lookup.get(structure)
        if structure_data is None:
            structure_lookup[structure] = str_dict
        else:
             structure_data.update(str_dict)
             structure_lookup[structure] = structure_data


str_data = data[0]
rng1.value


sht.range('A1').value
sht.range('A1:A5').value
sht.range('A1:E1').options(ndim=2).value
sht.book
test_book.name
rng1 = sht.range('A1').expand('table')
rng1.value
sht.name
test_book.close()
