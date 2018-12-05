import unittest
from pathlib import Path
import pandas as pd

from Tables import *

TableClassTests = unittest.TestSuite()
class Test_table_creation(unittest.TestCase):
    def test_creation_with_all_parameters(self):
        '''Test create table instant with all attributes defined'''
        file_path = Path(r'.\TablesTest.xlsx')
        sheet_name = 'Basic'
        title = 'Basic Table'
        offset = 'A1'
        index = 'label'
        columns = 3
        rows = 3
        new_table = Table(file_path, sheet_name, title, index, offset, columns, rows)
        self.assertEqual(new_table.file_path, file_path)
        self.assertEqual(new_table.sheet_name, sheet_name)
        self.assertEqual(new_table.title, title)
        self.assertEqual(new_table.index, index)
        self.assertEqual(new_table.offset, offset)
        self.assertEqual(new_table.columns, columns)
        self.assertEqual(new_table.rows, rows)

    def test_creation_with_default_parameters(self):
        '''Test create table instant with only required attributes defined'''
        file_path = Path(r'.\TablesTest.xlsx')
        sheet_name = 'Basic'
        new_table = Table(file_path, sheet_name)
        self.assertEqual(new_table.file_path, file_path)
        self.assertEqual(new_table.sheet_name, sheet_name)
        self.assertEqual(new_table.offset, 'A1')
        self.assertIsNone(new_table.title)
        self.assertIsNone(new_table.index)
        self.assertIsNone(new_table.columns)
        self.assertIsNone(new_table.columns)        
TableClassTests.addTest(Test_table_creation('test_creation_with_default_parameters'))
TableClassTests.addTest(Test_table_creation('test_creation_with_all_parameters'))

class Test_table_read(unittest.TestCase):
    def setUp(self):
        '''Use a single Test File'''
        self.file_path = Path(r'.\TablesTest.xlsx')
        self.test_excel_file = pd.ExcelFile(self.file_path)

    def tearDown(self):
        '''Close the Test file'''
        del self.test_excel_file

    def test_read_basic_table_direct_open(self):
        file_path = self.file_path
        sheet_name = 'Basic'
        title = 'Basic Table'
        offset = 'A1'
        index = 'label'
        columns = 3
        rows = 3
        new_table = Table(file_path=file_path, sheet_name=sheet_name, title=title, \
                          index=index, offset=offset, columns=columns, rows=rows)
        basic_table = new_table.read_table()
        test_df = pd.DataFrame([[1,'a'],[2,'b'],[3,'c']],index=['cat','dog','fish'],columns=["order","Values"])
        print(basic_table)
        print(test_df)
        self.assertTrue(basic_table.equals(test_df))

        #TODO add tests for integer - float conversion

    def test_read_basic_table(self):
        file_path = self.file_path
        sheet_name = 'Basic'
        title = 'Basic Table'
        offset = 'A1'
        index = 'label'
        columns = 3
        rows = 3
        new_table = Table(file_path=file_path, sheet_name=sheet_name, title=title, \
                          index=index, offset=offset, columns=columns, rows=rows)
        basic_table = new_table.read_table(self.test_excel_file)
        test_df = pd.DataFrame([[1,'a'],[2,'b'],[3,'c']],index=['cat','dog','fish'],columns=["order","Values"])
        print(basic_table)
        print(test_df)
        self.assertTrue(basic_table.equals(test_df))

    def test_read_basic_table_with_defaults(self):
        file_path = self.file_path
        sheet_name = 'Basic'
        title = 'Basic Table'
        new_table = Table(file_path=file_path, sheet_name=sheet_name, title=title)
        basic_table = new_table.read_table()
        test_df = pd.DataFrame([[1,'a','cat'],[2,'b','dog'],[3,'c','fish']],columns=["order","Values",'label'])
        print(basic_table)
        print(test_df)
        self.assertTrue(basic_table.equals(test_df))

    def test_read_table_with_no_title(self):
        file_path = self.file_path
        sheet_name = 'No Title'
        new_table = Table(file_path=file_path, sheet_name=sheet_name)
        basic_table = new_table.read_table()
        test_df = pd.DataFrame([[1,'a','cat'],[2,'b','dog'],[3,'c','fish']],columns=["order","Values",'label'])
        print(basic_table)
        print(test_df)
        self.assertTrue(basic_table.equals(test_df))

    def test_read_table_with_missing_values(self):
        file_path = self.file_path
        sheet_name = 'Missing Values'
        title = 'Missing Values Table'
        offset = 'A1'
        index = 'Index'
        columns = 3
        rows = 3
        new_table = Table(file_path=file_path, sheet_name=sheet_name, title=title, \
                          index=index, offset=offset, columns=columns, rows=rows)
        basic_table = new_table.read_table()
        test_df = pd.DataFrame([['a','a1'],['b',None],[None,'c2']],index=[1,2,3],columns=["Values1","Values2"])
        print(basic_table)
        print(test_df)
        self.assertTrue(basic_table.equals(test_df))

    def test_read_table_with_missing_values_in_bottom_right_corner(self):
        file_path = self.file_path
        sheet_name = 'Missing Corner'
        title = 'Missing Values Table'
        offset = 'A1'
        index = 'Index'
        columns = 3
        rows = 3
        new_table = Table(file_path=file_path, sheet_name=sheet_name, title=title, \
                          index=index, offset=offset, columns=columns, rows=rows)
        basic_table = new_table.read_table()
        test_df = pd.DataFrame([['a','a1'],['b','b2'],['c',None]],index=[1,2,3],columns=["Values1","Values2"])
        print(basic_table)
        print(test_df)
        self.assertTrue(basic_table.equals(test_df))

    def test_read_table_with_offset_from_A1(self):
        file_path = self.file_path
        sheet_name = 'Offset'
        title = 'Basic Table'
        offset = 'D4'
        columns = 2
        rows = 3
        new_table = Table(file_path=file_path, sheet_name=sheet_name, title=title, \
                          offset=offset, columns=columns, rows=rows)
        basic_table = new_table.read_table()
        test_df = pd.DataFrame([[1,'a'],[2,'b'],[3,'c']],columns=["Index","Values"])
        print(basic_table)
        print(test_df)
        self.assertTrue(basic_table.equals(test_df))

    def test_read_table_with_extra_data(self):
        file_path = self.file_path
        sheet_name = 'Extra Data'
        index = 'Index'
        title = 'Extra Data Table'
        offset = 'A1'
        columns = 3
        rows = 3
        new_table = Table(file_path=file_path, sheet_name=sheet_name, title=title, \
                          index=index, offset=offset, columns=columns, rows=rows)
        basic_table = new_table.read_table()
        test_df = pd.DataFrame([['a','a1'],['b',None],[None,'c2']],index=[1,2,3],columns=["Values1","Values2"])
        print(basic_table)
        print(test_df)
        self.assertTrue(basic_table.equals(test_df))
TableClassTests.addTest(Test_table_read('test_read_basic_table'))
TableClassTests.addTest(Test_table_read('test_read_basic_table_with_defaults'))
TableClassTests.addTest(Test_table_read('test_read_table_with_missing_values'))
TableClassTests.addTest(Test_table_read('test_read_table_with_missing_values_in_bottom_right_corner'))
TableClassTests.addTest(Test_table_read('test_read_table_with_offset_from_A1'))
TableClassTests.addTest(Test_table_read('test_read_table_with_extra_data'))

class Test_invalid_table_exception(unittest.TestCase):
    def setUp(self):
        '''Use a single Test File'''
        self.file_path = Path(r'.\TablesTest.xlsx')
        self.test_excel_file = pd.ExcelFile(self.file_path)

    def tearDown(self):
        '''Close the Test file'''
        del self.test_excel_file


    def test_missing_Spreadsheet(self):
        file_path = self.file_path.parent / 'missing_file.xlsx'
        sheet_name = 'Missing Title'
        title = 'Basic Table'
        new_table = Table(file_path=file_path, sheet_name=sheet_name, title=title)
        with self.assertRaises(MissingSpreadsheet):
             basic_table = new_table.read_table()

    def test_missing_worksheet(self):
        file_path = self.file_path
        sheet_name = 'Missing Sheet'
        title = 'Basic Table'
        new_table = Table(file_path=file_path, sheet_name=sheet_name, title=title)
        with self.assertRaises(MissingTable):
             basic_table = new_table.read_table()

    def test_missing_index(self):
        file_path = self.file_path
        sheet_name = 'Basic'
        title = 'Basic Table'
        index = 'no index'
        new_table = Table(file_path=file_path, sheet_name=sheet_name, title=title, index=index)
        with self.assertRaises(InvalidTable):
            basic_table = new_table.read_table(self.test_excel_file)

    def test_duplicate_index(self):
        file_path = self.file_path
        sheet_name = 'Basic'
        title = 'Duplicate Index'
        index = 'label'
        new_table = Table(file_path=file_path, sheet_name=sheet_name, title=title, index=index)
        with self.assertRaises(InvalidTable):
            basic_table = new_table.read_table(self.test_excel_file)

    def test_missing_title(self):
        file_path = self.file_path
        sheet_name = 'No Title'
        title = 'Basic Table'
        new_table = Table(file_path=file_path, sheet_name=sheet_name, title=title)
        with self.assertRaises(InvalidTable):
             basic_table = new_table.read_table(self.test_excel_file)

    def test_incorrect_title(self):
        file_path = self.file_path
        sheet_name = 'Basic'
        title = 'Wrong Table'
        new_table = Table(file_path=file_path, sheet_name=sheet_name, title=title)
        with self.assertRaises(InvalidTable):
            basic_table = new_table.read_table(self.test_excel_file)
    

#    def test_invalid_header_values(self):
#        self.fail("Not implemented")

#    def test_unexpected_location(self):
#        self.fail("Not implemented")
    
#    def test_too_many_columns(self):
#        self.fail("Not implemented")
    
#    def test_too_few_columns(self):
#        self.fail("Not implemented")
    
#    def test_too_many_rows(self):
#        self.fail("Not implemented")
    
#    def test_too_few_rows(self):
#        self.fail("Not implemented")
    
#TableClassTests.addTest(Test_invalid_table_exception('test_too_few_rows'))
#TableClassTests.addTest(Test_invalid_table_exception('test_missing_header_values'))
#TableClassTests.addTest(Test_invalid_table_exception('test_invalid_header_values'))
#TableClassTests.addTest(Test_invalid_table_exception('test_missing_index'))
#TableClassTests.addTest(Test_invalid_table_exception('test_duplicate_index'))

    def test_missing_header_value(self):
        file_path = self.file_path
        sheet_name = 'Missing Header'
        title = 'Missing Header'
        new_table = Table(file_path=file_path, sheet_name=sheet_name, title=title)
        with self.assertRaises(InvalidTable):
            basic_table = new_table.read_table(self.test_excel_file)
            print(basic_table)        
TableClassTests.addTest(Test_invalid_table_exception('test_missing_Spreadsheet'))
TableClassTests.addTest(Test_invalid_table_exception('test_missing_worksheet'))
TableClassTests.addTest(Test_invalid_table_exception('test_missing_index'))
TableClassTests.addTest(Test_invalid_table_exception('test_duplicate_index'))
TableClassTests.addTest(Test_invalid_table_exception('test_missing_title'))
TableClassTests.addTest(Test_invalid_table_exception('test_incorrect_title'))

VariableClassTests = unittest.TestSuite()
class Test_Variable_creation(unittest.TestCase):

#TODO add tests for exceptions raised in Variable class

    def test_creation_with_all_parameters(self):
        '''Test create Variable instance with all attributes defined'''
        ID = 'TestAttr'
        variable_type = VARIABLE_TYPES[0]
        validate = always_true
        default = 'Default Value'
        test_attr = Variable(ID, variable_type, validate, default)
        self.assertEqual(test_attr.ID, ID)
        self.assertEqual(test_attr.variable_type, variable_type)
        self.assertEqual(test_attr.validate, validate)
        self.assertEqual(test_attr.default, default)

    def test_creation_without_default_parameter(self):
        '''Test create TemplateAttribute instance with only required attributes defined'''
        ID = 'TestAttr'
        variable_type = VARIABLE_TYPES[0]
        validate = always_true
        test_attr = Variable(ID, variable_type, validate)
        self.assertEqual(test_attr.ID, ID)
        self.assertEqual(test_attr.variable_type, variable_type)
        self.assertEqual(test_attr.validate, validate)
        self.assertIsNone(test_attr.default)    
VariableClassTests.addTest(Test_Variable_creation('test_creation_without_default_parameter'))
VariableClassTests.addTest(Test_Variable_creation('test_creation_with_all_parameters'))

TableOperationsTests = unittest.TestSuite()
class TestTableImporting(unittest.TestCase):
    def setUp(self):
        '''Define Tables and Variables
        '''
        self.file_path = file_path = Path(r'.\TablesTest.xlsx')
        sheet_name = 'Basic'
        title = 'Basic Table'
        offset = 'A1'
        index = 'label'
        columns = 3
        rows = 3
        self.basic_table = Table(file_path, sheet_name, title, index, offset, columns, rows)
        self.second_table = Table(file_path, 'Second', 'Second Table', index, offset, columns, rows)
        self.third_table = Table(file_path, 'Third', 'Third Table', index, offset, columns, rows)
        self.defaults_table = Table(file_path, 'defaults', 'Default Values Table', index, offset, columns)
        variable_names = [('order', 'ox'), \
                          ('Values', 'x'), \
                          ('Values1', 'x1'), \
                          ('Values2', 'x2'), \
                          ('Values3', 'x3'), \
                          ('Values4', 'x4'), \
                          ('Values5', None)]
        self.variables_list = {ID: Variable(ID, VARIABLE_TYPES[0], default=dflt) 
                               for (ID, dflt) in variable_names}

        self.df_basic = pd.DataFrame([[1,'a'],[2,'b'],[3,'c']],index=['cat','dog','fish'],columns=["order","Values"])
        self.df_second = pd.DataFrame([['foo1','blue'],['boo2'],['bob3','red']],index=['cat','dog','fish'],columns=["Values3","Values2"])
        self.df_third = pd.DataFrame([['A3','R1'],['B3','R2'],['C3']],index=['cat','dog','fish'],columns=["Values4","Values5"])
        self.df_defaults = pd.DataFrame([['a','a1'],['b'],[None,'c2'],['d','d1'],['x','x1']], \
            index=['cat','dog','fish','bird','default'],columns=["Values1","Values2"])
        self.new_defaults = {'Values1': 'x', 'Values2': 'x1'}

    def tearDown(self):
        '''Close the Test file'''
        pass
        
    def test_select_one_variable(self):
        '''Test selection of columns from an imported table
        '''
        variable = {'Values': Variable('Values', VARIABLE_TYPES[0])}
        table = self.basic_table.read_table()
        selected_table = select_variables(table, variable)
        print(type(selected_table))
        print(selected_table)
        df_one = pd.DataFrame(self.df_basic.loc[:,'Values'])
        print(df_one)
        self.assertTrue(selected_table.equals(df_one))

    #TODO Add more tests for selecting multiple variables
    #TODO Add more tests for extraneous data in the worksheet

    def test_merge_tables_with_one_column_dropped(self):
        '''Test merging of multiple tables
        '''
        table_list = [self.basic_table, self.second_table, self.third_table]
        variables_used = self.variables_list.copy()
        del variables_used['Values3']
        test_table = merge_tables(self.file_path, table_list, variables_used)
        test_table.sort_index(axis=1, inplace=True)
        print(test_table)
        df_list = [self.df_basic, self.df_second.drop('Values3',axis=1), self.df_third]
        test_pd = pd.DataFrame()
        test_pd = test_pd.join(df_list, how='outer')
        test_pd.sort_index(axis=1, inplace=True)
        print(test_pd)
        self.assertTrue(test_table.equals(test_pd))

    def test_merge_tables_with_missing_and_extra_values(self):
        '''Test merging of multiple tables with some tables having additional 
        rows and other rows having missing values.
        '''
        table_list = [self.third_table, self.defaults_table]
        test_table = merge_tables(self.file_path, table_list, self.variables_list)
        test_table.sort_index(axis=1, inplace=True)
        print(test_table)
        df_list = [self.df_third, self.df_defaults]
        test_pd = pd.DataFrame()
        test_pd = test_pd.join(df_list, how='outer')
        test_pd.sort_index(axis=1, inplace=True)
        print(test_pd)
        self.assertTrue(test_table.equals(test_pd))

    def test_select_multiple_variable(self):
        '''Test selection of columns from an imported table
        '''
        df_list = [self.df_third, self.df_second]
        Initial_pd = pd.DataFrame()
        Initial_pd = Initial_pd.join(df_list, how='outer')
        Initial_pd.sort_index(axis=1, inplace=True)
        print(Initial_pd)
        variables = self.variables_list
        del variables['Values5']
        del variables['Values2']
        selected_table = select_variables(Initial_pd, variables)
        selected_table.sort_index(axis=1, inplace=True)
        print(selected_table)
        test_pd = pd.DataFrame()
        test_pd = test_pd.join([self.df_second['Values3'], self.df_third['Values4']], how='outer')
        self.assertTrue(selected_table.equals(test_pd))

    def test_merge_tables_with_duplicate_variables(self):
        '''Test merging of multiple tables with one variable in more than one table.
        '''
        table_list = [self.second_table, self.defaults_table]
        with self.assertRaises(InvalidVariable):
            test_table = merge_tables(self.file_path, table_list, self.variables_list)

    def test_process_defaults(self):
        '''Test setting variable defaults from table
        '''
        df_list = [self.df_third, self.df_defaults]
        test_pd = pd.DataFrame()
        test_pd = test_pd.join(df_list, how='outer')
        for var in self.variables_list.values():
            print('Variable: {}, Defaults Value {}\n'.format(var.ID, var.default))
        print(test_pd)
        original_defaults = {var.ID: var.default for var in self.variables_list.values()}
        updated_variables_list = process_defaults(test_pd, self.variables_list)
        updated_defaults = {var.ID: var.default for var in updated_variables_list.values()}
        for var in updated_variables_list.values():
            print('Variable: {}, Defaults Value {}\n'.format(var.ID, var.default))
        test_defaults = original_defaults
        test_defaults.update(self.new_defaults)
        self.assertDictEqual(updated_defaults,test_defaults)

    def test_process_no_defaults(self):
        '''Test setting variable defaults from table
        '''
        test_pd = self.df_third
        for var in self.variables_list.values():
            print('Variable: \t{}, \tDefaults Value \t{}'.format(var.ID, var.default))
        print(test_pd)
        test_defaults = {var.ID: var.default for var in self.variables_list.values()}
        updated_variables_list = process_defaults(test_pd, self.variables_list)
        updated_defaults = {var.ID: var.default for var in updated_variables_list.values()}
        for var in updated_variables_list.values():
            print('Variable: \t{}, \tDefaults Value \t{}'.format(var.ID, var.default))
        self.assertDictEqual(updated_defaults,test_defaults)

    def test_update_missing_values(self):
        '''Test merging of multiple tables with some tables having additional 
        rows and other rows having missing values.
        '''
        df_list = [self.df_third, self.df_second]
        Initial_pd = pd.DataFrame()
        Initial_pd = Initial_pd.join(df_list, how='outer')
        Initial_pd.sort_index(axis=1, inplace=True)
        print(Initial_pd)
        test_pd = Initial_pd.copy()
        test_pd.loc['dog','Values2'] = self.variables_list['Values2'].default
        print(test_pd)
        updated_pd = insert_defaults(Initial_pd, self.variables_list)
        print(updated_pd)
        updated_pd.sort_index(axis=1, inplace=True)
        self.assertTrue(test_pd.equals(updated_pd))

    def test_insert_missing_variables(self):
        '''Test adding variables with their default values for variables 
        in a list which are not found in the table.
       '''
        df_list = [self.df_basic, self.df_second]
        Initial_pd = pd.DataFrame()
        Initial_pd = Initial_pd.join(df_list, how='outer')
        Initial_pd.sort_index(axis=1, inplace=True)
        print(Initial_pd)
        test_pd = Initial_pd.copy()
        test_pd['Values1'] = self.variables_list['Values1'].default
        test_pd['Values4'] = self.variables_list['Values4'].default
        test_pd.sort_index(axis=1, inplace=True)
        print(test_pd)
        updated_pd = insert_missing_variables(Initial_pd, self.variables_list)
        updated_pd.sort_index(axis=1, inplace=True)
        print(updated_pd)
        self.assertTrue(test_pd.equals(updated_pd))
TableOperationsTests.addTest(TestTableImporting('test_select_one_variable'))
TableOperationsTests.addTest(TestTableImporting('test_merge_tables_with_one_column_dropped'))
TableOperationsTests.addTest(TestTableImporting('test_merge_tables_with_missing_and_extra_values'))
TableOperationsTests.addTest(TestTableImporting('test_merge_tables_with_duplicate_variables'))
TableOperationsTests.addTest(TestTableImporting('test_process_defaults'))
TableOperationsTests.addTest(TestTableImporting('test_process_no_defaults'))
TableOperationsTests.addTest(TestTableImporting('test_update_missing_values'))
TableOperationsTests.addTest(TestTableImporting('test_insert_missing_variables'))



if __name__ == '__main__':
    unittest.main()
