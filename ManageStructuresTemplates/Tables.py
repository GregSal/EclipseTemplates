'''Define, Import and Manage Spreadsheet Tables
'''

from pathlib import Path
import re
import pandas as pd


class TableException(Exception): pass
class InvalidTable(TableException): pass
class MissingTable(TableException): pass
class MissingSpreadsheet(TableException): pass
class InvalidVariable(TableException): pass
class VariableNotSet(TableException): pass

always_true = lambda x: True

global VARIABLE_TYPES, DEFAULT_INDEX
VARIABLE_TYPES = ['Default']
DEFAULT_INDEX = 'default'

def xl_to_xy(xl: str):
    '''Convert excel style "A1" indexing to x,y offset
    Parameter
        xl: Type str
            A string of the format "A1"
    Returns
        A length 2 tuple (columns, rows) indicating the offset from A1
        e.g. 'A1' returns (0,0)
    Raises
        ValueError exception
    '''
    pattern = re.compile('^([A-Z]+)([0-9]+)$')
    match = pattern.match(xl)
    if match is None:
        raise ValueError(str(xl) + ' is not a valid excel index')
    col = match.group(1)
    #Convert sequence of letters to number
    # ord('A') = 65
    column_offset = sum((ord(l)-65)*26**n for (n, l) in enumerate(col))
    row = match.group(2)
    row_offset = int(row)-1
    if row_offset < 0:
        raise ValueError(str(xl) + ' is not a valid excel index')
    return (column_offset, row_offset)
#TODO add a conversion from XY to A1
#TODO make A1 to/from XY conversions sub functions of Table class

def get_value(definitions, key_name):
    '''return the requested value from a dictionary or series, testing for undefined items.
    If the requested value is not found in either dictionary ValueError is raised.
    '''
    if key_name in definitions:
        value = str(definitions.get(key_name))
    else:
        raise VariableNotSet('A value for {} was not given'.format(key_name))
    #Check for NaN, which indicates that a value was not supplied
    if value != value:
        raise VariableNotSet('A value for {} was not given'.format(key_name))
    return value

class Table(object):
    '''Defines, Import and Manage Spreadsheet Tables

    Attributes
        file_path:  The path to the spreadsheet file
        sheet_name: The name of the worksheet in the excel file
        title:      The title of the table as found in the top cell,
                        if None, no table title should be present
        offset:     The expected offset as an (columns,rows) tuple
                    or in the A1 format,
                        if None, A1 is used
        columns     An expected range of columns,
                        if None, # columns testing is not done
        rows        An expected range of columns,
                        if None, # rows testing is not done
        index:      The header string of the index column
                        if None, no index is assigned
        variables:  A list of the expected names of the column variables
                        if None, column headers are not checked
    Methods
        __init__
			Set attributes
			Verify that attributes are reasonable
        read Table
			read in the table data from the worksheet
            set index if defined
			Test that the table is valid based on the table attributes defined
    Raises
        MissingSpreadsheet
        MissingTable
        InvalidTable
        '''
        #TODO update calls to Table() to include variables list
        #Some are done but others are not
    def __init__(self, file_path: Path, sheet_name: str, title=None, \
                 index=None, offset='A1', columns=None, rows=None, variables=None):
        '''Define Table instance, set attributes and verify that attributes are reasonable
        Parameters
            file_path:  Required,   Type Path,
                The path to the spreadsheet file
            sheet_name: Required,   Type str
                The name of the worksheet in the excel file
		    title:      Optional,   Type str
                The title of the table as found in the top cell,
                    if None, no table title should be present
		    offset:      Optional,   Type 2 element tuple or str in A1 format
                The expected offset to the top right corner of the table,
                    if None, A1 is used
		    columns:     Optional,   Type integer or range
                An expected range of columns,
                    if None, # columns testing is not done
		    rows:     Optional,   Type integer or range
                An expected range of columns,
                    if None, # rows testing is not done
		    index:     Optional,   Type str
                The header string of the index column
                    if None, no index is assigned
        Raises
            Type Error
            Value Error
        '''
# TODO add comments regarding variables parameter
        if isinstance(file_path,Path):
            self.file_path = file_path
        else:
            raise TypeError('file_path must be type Path, got type: ' + type(file_path))

        if isinstance(sheet_name,str):
            self.sheet_name = sheet_name
        else:
            raise TypeError('sheet_name must be type str, got type: ' + type(sheet_name))

        if title is None:
            self.title = None
        else:
            if isinstance(title,str):
                self.title = title
            else:
                raise TypeError('title must be type str, got type: ' + type(title))

        if isinstance(offset,str):
            # ToDo Test offset for A1 format
            self.offset = offset
        elif isinstance(offset,tuple):
            raise NotImplementedError('offset as tuple not yet implemented')
        else:
            raise TypeError('offset must be in the "A1" format')

        if index is None:
            self.index = None
        else:
            if isinstance(index,str):
                self.index = index
            else:
                raise TypeError('index must be type str, got type: ' + type(index))

        if columns is None:
            self.columns = None
        else:
            if isinstance(columns,int):
                self.columns = columns
            elif isinstance(columns,range):
                raise NotImplementedError('columns as range not yet implemented')
                self.columns = columns
            else:
                raise TypeError('columns must be type int or range, got type: ' + type(columns))
# FIX ME type(...) needs to be changed to str(type(...))
        if rows is None:
            self.rows = None
        else:
            if isinstance(rows,int):
                self.rows = rows
            elif isinstance(rows,range):
                raise NotImplementedError('rows as range not yet implemented')
                self.rows = rows
            else:
                raise TypeError('rows must be type int or range, got type: ' + type(rows))

        if variables is None:
            self.variables = None
        else:
            if isinstance(variables,dict):
                self.variables = variables
            else:
                raise TypeError('variables must be type dict, got type: ' + type(variables))

    def read_table(self, workbook=None, drop_missing=True):
        '''read in the table data from a worksheet
           set index if defined
        Parameters
            workbook    Optional,   Type Pandas ExcelFile
				The workbook containing the sheet with the table
            drop_missing    Optional,   Type boolean
                If true remove rows containing all missing values
        Returns
            Table data as a Pandas data-frame
        '''
        #TODO update read_table doc string
        #TODO include the resulting DataFrame as a Table attribute
        # Check for table offset from A1
        (column_offset, row_offset) = xl_to_xy(self.offset)
        if self.columns is not None:
            selected_columns = [i for i in
                    range(column_offset, column_offset+self.columns)]
        else:
            selected_columns = None
        if workbook is None:
            table_file = self.file_path
            if not table_file.exists():
                raise MissingSpreadsheet('File {} does not exist.'.format(table_file))
            workbook = pd.ExcelFile(table_file)

        # Check that worksheet exists
        sheet_list = workbook.sheet_names
        if not self.sheet_name in sheet_list:
            raise MissingTable('{} is not a valid sheet name'.format(self.sheet_name))

        # Set offset
        if self.title is None:
            header_offset = row_offset
        else:
            header_offset = row_offset+1

        # Add conversion functions
        if self.variables is None:
            var_cnv = None
        else:
            var_cnv = {v.ID: v.conversion for v in self.variables.values()
                       if v.conversion is not None}

        # Read table
        table_data = pd.read_excel(workbook, self.sheet_name, \
                                header=header_offset, \
                                usecols=selected_columns, \
                                converters=var_cnv)

        #Check table title
        if self.title is not None:
            title = pd.read_excel(workbook, self.sheet_name, \
                                    skiprows=row_offset, \
                                    usecols=selected_columns, \
                                    skipfooter=len(table_data)+1).columns[0]
            if self.title not in title:
                raise InvalidTable('Title Mismatch: expecting {}, found {}'.format(self.title,title))
        # Check for missing header variables
        headers = list(table_data.columns.values)
        if any('Unnamed' in header for header in headers):
            raise InvalidTable('Missing header')

        #Remove empty rows
        #TODO make drop rows a separate method
        if drop_missing:
            table_data.dropna(axis=0, how='all', inplace=True)

        # Set index column
        if self.index is not None:
            try:
                table_data.set_index(self.index, inplace=True, verify_integrity=True)
            except KeyError:
                raise InvalidTable('Index error')

        return table_data

class Variable(object):
    '''Defines, and validates Table Variables

    Attributes
        ID:             Name of variable Type str
        variable_type:  The variable category.  Must member of VARIABLE_TYPES global tuple
		default:        Default value for the variable.
                        If None, The variable value must always be explicitly given.
        validate:       A one parameter function that returns a boolean indicating
                        if the variable value is valid.  Called in check_values.
                        If not set value checking is not done
        conversion      Method to convert data type, currently forces string conversion
    Methods
        __init__
			Set attributes
			Verify that attributes are reasonable
        check_value
            apply validate function(s) to value parameters
        update_default
            if valid, replaces current default with new default value
    Raises
        InvalidVariable
        '''

#TODO add a convert attribute to Variable that will be used to convert the Excel value
#In particular this would be used to set the correct data type e.g. str() or int()
#Currently forces string conversion
    def __init__(self, ID: str, variable_type: str, validate=always_true, default=None):
        '''Define Variable instance, set type, default and validate function
        Parameters
            ID:             Required,   Type str with no spaces
                            Name of variable (Table header) Type str
            variable_type:  Required,   Type str
                            The variable category.  Must member of VARIABLE_TYPES global tuple
            validate:       Optional,   Type callable
                            A one parameter function that returns a boolean indicating
                            if the variable value is valid.  Called in check_values.
		    default:        Optional,
                            Default value for the variable.
                            If None, The variable value must always be explicitly given.
        Raises
            Type Error
            Value Error
        '''
        if isinstance(ID,str):
            if ' ' not in ID:
                self.ID = ID
            else:
                raise ValueError('ID must not contain any spaces')
        else:
            raise TypeError('ID must be type str, got type: ' + type(ID))

        if isinstance(variable_type,str):
            if any(t in variable_type for t in VARIABLE_TYPES):
                self.variable_type = variable_type
            else:
                raise ValueError('variable_type must be one of: {}'.format(', '.join(VARIABLE_TYPES)))
        else:
            raise TypeError('variable_type must be type str, got type: ' + type(variable_type))

        if validate is None:
            self.validate = always_true
        else:
            if callable(validate):
                self.validate = validate
            else:
                raise TypeError('validate must be a one parameter function that returns a boolean')

        if default is None:
            self.default = None
        elif self.validate(default):
            self.default = default

        # TODO Allow for other data conversion types
        self.conversion = str

    def check_value(self, value):
        '''Apply validate function(s) to value parameters.
        If value is None, return True
        Returns
            boolean indicating if value is valid for this attribute
        '''
        if value is None:
            return True
        else:
           return self.validate(value)

    def update_default(self, value):
        '''If valid, update default with value.
        If value is None, no testing is done.
       Raises
            InvalidVariable
        '''
        if value is None:
            self.default = None
        elif self.validate(value):
            self.default = value
        else:
            raise InvalidVariable('{} is not a valid value for {}'.format(value, self.ID))

def select_variables(table, variables):
    '''Selects the variables found in table and checks that its values are valid
	Parameters
		table:
            Required,   Type DataFrame
        variables:
                Required,   Type dict,
                A dict of Variable definitions that may be found as columns
                in the table.
    Returns:
        A subset of table containing only the columns found in variables or
        None if no columns found.
	Raises
	    InvalidAttribute
    '''
    #select variables Make this a Table method
    # find columns with specified variables
    table_variables = set(table.columns.values)
    columns = list()
    for var_name in table_variables:
        var = variables.get(var_name)
        if var is not None:
            #Check that variable data is valid
            if not all(var.check_value(value) for value in table[var_name]):
                raise InvalidVariable('{} in table {} contains an invalid value'.format(var.ID,  table.title))
            else:
                columns.append(var_name)
    if len(columns) > 0:
       return table.loc[:,columns]
    else:
        return None

def merge_tables(spreadsheet_file, tables_list, variables_list=None):
    '''Reads in, validates and merges a list of tables
    Only variables in the variables dictionary are merged
	Parameters
		spreadsheet_file:
                Required,   Type Path,
                The path to the spreadsheet file
        tables_list:
                Required,   Type list,
                A list of the Table objects defining each required table
                Note: all tables should have the same index defined
                Other than the index variable, no other variable should
                occur in more than one table.
        variables_list:
                Optional,   Type dict,
                A dict of the Variable objects defining each table variable
    Returns
		merged_table:
            A Pandas data-frame created by merging all excel tables read in
	Raises
		MissingSpreadsheet
        MissingTable
	    InvalidAttribute
    '''
    #Initialize lists
    variables_imported = list()
    dataframe_list = list()
    # Check that spreadsheet file exists
    if not spreadsheet_file.exists():
        raise MissingSpreadsheet('File {} does not exist.'.format(str(spreadsheet_file)))
    with pd.ExcelFile(spreadsheet_file) as workbook:
        sheet_list = workbook.sheet_names
        for table in tables_list:
            # Check that worksheet exists
            if not table.sheet_name in sheet_list:
                raise MissingTable('table: {} cannot be found in the file: {}'.format(table, str(spreadsheet_file)))
            data_table = table.read_table(workbook)
            if variables_list is not None:
                # Select and test variables
                selected_table = select_variables(data_table, variables_list)
            else:
                selected_table = data_table
            if selected_table is not None:
                found_variables = list(selected_table.columns.values)
                # Check that variable is not already in a table
                duplicates = [var for var in found_variables
                              if var in variables_imported]
                if len(duplicates) > 0:
                    raise InvalidVariable('The variable {} in table {} has already been read in from another table'.format(duplicates[0], table.title))
                #Add table and variables to lists
                variables_imported.extend(found_variables)
                dataframe_list.append(selected_table)
    #Merge the tables
    merged_table = pd.DataFrame()
    merged_table = merged_table.join(dataframe_list, how='outer')
    return merged_table

def process_defaults(table: pd.DataFrame, variables: dict):
    '''Searches for 'default' in the index and updates the default value for
    each variable that contains a valid value.
    Parameters
		table:
                Required,   Type DataFrame,
                The table to be searched.
        variables:
                Required,   Type dict,
                A dictionary of the Variable objects found in table to be updated.
    Returns
		updated_variables:
            The variables_list with updated default values.
            The method does not return a deep copy so the new list returned
            will be pointing to the original Variable objects.
    '''
    #TODO make process_defaults a Table method
    # Consider including a deep copy, but to be effective a __deepcopy__ method
    # would need to be added to the Variables class.
    updated_variables = variables
    try:
        default_values = table.loc[DEFAULT_INDEX]
    except KeyError:
        # If Default is not found in the index, don't do anything
        return updated_variables
    else:
        values_set = ~default_values.isnull()
        for (variable_name, value) in default_values[values_set].iteritems():
            var = variables.get(variable_name)
            if var is not None:
                var.update_default(value)
                updated_variables[variable_name]  = var
        return updated_variables

def insert_defaults(table: pd.DataFrame, variables: list):
    '''Replaces null values (None/NaN) in a DataFrame with the corresponding
    default value from the variables.
    If a default value is not found (is None) the null is not changed
    Parameters
		table:
                Required,   Type DataFrame,
                The table to be searched.
        variables:
                Required,   Type dict,
                The dictionary of Variable objects containing the default values.
    Returns
		updated_table:
            A copy of the table DataFrame with null values replaced with
            default values.
    '''
    #TODO make insert_defaults a Table method
    #TODO there is probably significant room for optimization
    updated_table = table.copy()
    # select columns with specified variables
    table_variables = set(table.columns.values)
    for (var_name, data) in table.iteritems():
        var = variables.get(var_name)
        if var is not None:
            if var.default is not None:
                updated_table[var_name] = data.fillna(value=var.default)
    return updated_table

def insert_missing_variables(table: pd.DataFrame, variables: list):
    '''Adds default values from variables list for all variables not found
    in the table.
    If a missing variable does not have a default value it is not added to
    the table.
    Parameters
		table:
                Required,   Type DataFrame,
                The table to be expanded with missing variables.
        variables:
                Required,   Type dict,
                The dictionary of Variable objects containing the default
                values.
    Returns
		updated_table:
            A copy of the table DataFrame with the default values of the
            missing variables added.
    '''
    #TODO make insert_missing_variables a Table method
    updated_table = table.copy()
    # identify the missing variables
    variables_list = set(var_name for var_name in variables)
    table_variables = set(table.columns.values)
    missing_variables = variables_list - table_variables
    for var in missing_variables:
        if variables[var].default is not None:
            updated_table[var] =  variables[var].default
    return updated_table

if __name__ == '__main__':
    #from Tables import *
    file_path = Path(r'.\TablesTest.xlsx')
    sheet_name = 'Basic'
    title = 'Basic Table'
    offset = 'A1'
    index = 'label'
    columns = 3
    rows = 3
    new_table = Table(file_path, sheet_name, title, index, offset, columns, rows)
    basic_table = new_table.read_table()
    print(basic_table)
    df = pd.DataFrame([[1,'a'],[2,'b'],[3,'c']],index=['cat','dog','fish'],columns=["order","Values"])
    print(df)
    df.equals(basic_table)
    a = Table(file_path, sheet_name, title, 'blue', offset, columns, rows)
    basic_table = a.read_table()