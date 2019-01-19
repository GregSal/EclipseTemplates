"""
Created on Mon Jan 7 2018

@author: Greg Salomons
"""
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import utilities_path
from file_utilities import set_base_dir
from SelectTemplates import import_template_list
from spreadsheet_tools import load_reference_table
#base_path = set_base_dir()
#active_templates = import_template_list(base_path)

all_template_vars = ['workbook_name', 'sheet_name', 'title',
                     'columns', 'output_file_name', 'in_use']

template_vars = ['workbook_name', 'title']

template_file_info = dict(file_name='Template List.xlsx',
                          sub_dir=r'Work\Structure Dictionary\Template Spreadsheets',
                          sheet_name='templates')
template_table_info = dict(starting_cell='A1', header=1)

template_selections = dict(unique_scans=['title'],
                           select_columns=template_vars,
                           criteria_selection={'in_use': True})

# 'workbook_name': 'Basic Templates.xlsx',
def print_selection():
        select_list = [str(item) for item in template_selector.selection()]
        select_str = '\n'.join(select_list)
        messagebox.showinfo('Selected Templates', select_str)

root = tk.Tk()
root.title("Template Selection")
style = ttk.Style()
style.theme_use('vista')
# tree = ttk.Treeview(root, columns=template_vars)
template_selector = ttk.Treeview(root)
template_selector.insert('', 'end', 'templates', text='Structure Templates')

active_templates = load_reference_table(template_file_info, template_table_info, **template_selections)
workbooks = active_templates.groupby('workbook_name')
for workbook, sheets in workbooks:
        workbook_str = workbook.split('.', 1)[0]
        template_selector.insert('templates', 'end', workbook_str,
                                 text=workbook_str, tags=('File'))
        for template in sheets.itertuples():
                template_selector.insert(workbook_str, 'end', template.title,
                                         text=template.title, tags=('Template'))
template_selector.tag_configure('File', foreground='blue', background='light grey')
template_selector.pack()
selection_button = ttk.Button(root, text='Show Selected', command=print_selection)
selection_button.pack()
root.mainloop()

#values = template_selector.selection()
#showinfo(title, message, options)
#whatever_you_do = "Whatever you do will be insignificant, but it is very important that you do it.\n(Mahatma Gandhi)"
#msg = tk.Message(master, text = whatever_you_do)
#msg.config(bg='lightgreen', font=('times', 24, 'italic'))
#msg.pack()


# root.geometry('350x200')

# Same thing, but inserted as first child:
# template_selector.insert('', 0, 'gallery', text='Applications')
# Treeview chooses the id:
# id = template_selector.insert('', 'end', text='Tutorial')
# tree.move('widgets', 'gallery', 'end')  # move widgets under gallery
# tree.detach('widgets')
# tree.delete('widgets')
# tree.item('widgets', open=True)
# isopen = tree.item('widgets', 'open')
# template_selector['columns'] = ('size', 'modified', 'owner')
# template_selector.column('size', width=100, anchor='center')
# template_selector.heading('size', text='Size')
# template_selector.set('widgets', 'size', '12KB')
# size = template_selector.set('widgets', 'size')
# template_selector.insert('', 'end', text='Listbox', values=('15KB Yesterday mark'))
# template_selector.insert('', 'end', text='button', tags=('ttk', 'simple'))
# template_selector.tag_configure('ttk', background='yellow')
# template_selector.tag_bind('ttk', '<1>', itemClicked)  # the item clicked can be found via tree.focus()
