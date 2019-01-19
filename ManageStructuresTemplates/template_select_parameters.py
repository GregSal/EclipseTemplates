'''
Created on Aug 11 2017

@author: Greg Salomons
Define parameters required for building Structure Templates.

Warnings
    NameInUse:
        An output file or sheet name is already in use.
    InvalidPath:
        The given path is not a valid selection.
Exceptions
    NameInUse:
        An output file or sheet name is already in use.
    InvalidPath:
        The given path is not a valid selection.
    FileTypeError:
        The file extension is not the appropriate type.
    SelectionError:
        The string contents are not valid.
Classes
    ParametersBase: Base class for parameter objects.
    template_selection:  Input parameters required for building Structure Templates.

Functions
    valid_dir:
        Convert string to path if required, check that the path is an
        existing directory and return the full path.
    valid_file:
        Convert string to path if required, check that the path is an
        exiting file and return the full path.
    valid_sheet_name
        Check that the supplied sheet_name is valid.
'''
# TODO Convert to VariableSet
from pathlib import Path
from typing import Dict, Union, List
import warnings
from file_utilities import FileTypes

# TODO Convert to Custom Variable Set
# TODO Add 	Show inactive variable

#Warning and Exception definitions
class ParameterWarning(UserWarning):
    '''Base warning for setting and getting parameters.
    '''
    pass
class ParameterError(Exception):
    '''Base exception for setting and getting parameters.
    '''
    pass
class NameInUse(ParameterWarning):
    '''An output file or sheet name is already in use.
    '''
    pass
class InvalidPath(ParameterWarning):
    '''The given path is not a valid selection.
    '''
    pass
class FileTypeError(ParameterError, FileNotFoundError):
    '''The file extension is not the appropriate type.
    '''
    pass
class SelectionError(ParameterError, TypeError):
    '''The string contents are not valid.
    '''
    pass


def valid_sheet_name(sheet_name: str):
    ''' Check that the supplied sheet_name is valid.
    Parameter
        sheet_name: Type str
            An excel worksheet name.
    Returns
        A full path to an existing file of type Path
    Raises
        TypeError exception
    '''
    if not isinstance(sheet_name, str):
        raise TypeError('The sheet name must be Type str')
    else:
        #ToDo Add legal worksheet name tests
        return True

class ParametersBase(object):
    '''Base class for parameter objects used by DirScan.
    Class Attributes:
        base_path
            Type: Path
            The starting path to use for incomplete file and directory
            parameters
            Default = Path.cwd()
    Instance Attributes:
        parameters_valid
            Type bool
            Indicate whether the parameters object contains validated
            parameters.
            Default = True
    Methods
        valid_dir(dir_path: Path, exist=True):
            Static method
            Check that the supplied path exists and is a directory.
        valid_file(file_path: Path, exist=True):
            Static method
            Check that the supplied path exists and is a file.
        __init__(base_path=None, **kwargs):
			Set attributes
			Verify that attributes are reasonable
        insert_base_path(file_name: str):
            Add the base path to a filename or relative string path and
            return a full path to a file or directory of type Path.
        update_parameters(base_path=None, **kwargs)
            Update any supplied parameters by calling the relevant method.

        The following methods are used to test and modify individual
        parameter attributes:
            update_base_path(directory_path: Path):
                Update the base path used to complete any file name or partial
                paths.
        The following methods set boolean options to True or False
            set_parameters_valid(is_valid: bool):
                Indicate whether the parameters object contains validated
                parameters.
    '''
	# Initialize class level parameters
    base_path = Path.cwd()

    # Methods to check directories, files and sheet names
    @staticmethod
    def valid_dir(dir_path: Path, exist=True):
        ''' If dir_path is a string convert it to type Path.
            Resolve any relative path parts.
            Check that the supplied path exists and is a directory.
        Parameters:
            dir_path: Type Path or str
                a relative or full path to a directory
            exist: Type bool
                Check whether the directory exists
        Returns
            A full path to an existing directory of type Path
        Raises
            TypeError exception
            NotADirectoryError exception
        '''
        if isinstance(dir_path, Path):
            full_directory_path = dir_path.resolve()
        elif isinstance(dir_path, str):
            full_directory_path = Path(dir_path).resolve()
        else:
            raise TypeError('The directory path must be Type Path or str')
        if exist:
            if full_directory_path.is_dir():
                return full_directory_path
            else:
                raise NotADirectoryError(\
                    'The directory path must refer to an existing directory')
        else:
            return full_directory_path

    @staticmethod
    def valid_file(file_path: Path, exist=True):
        ''' If file_path is a string convert it to type Path.
            Resolve any relative path parts.
            Check that the supplied path exists and is a file.
        Parameters
            file_path: Type Path or str
                a relative or full path to a file
            exist: Type bool
                Check whether the file exists
        Returns
            A full path to an existing file of type Path
        Raises
            TypeError exception
            FileNotFoundError exception
        '''
        if isinstance(file_path, Path):
            full_file_path = file_path.resolve()
        elif isinstance(file_path, str):
            full_file_path = Path(file_path).resolve()
        else:
            raise TypeError('The file path must be Type Path or str')
        if exist:
            if full_file_path.exists():
                return full_file_path
            else:
                msg = 'The file path must refer to an existing file'
                raise FileNotFoundError(msg)
        else:
            return full_file_path


    def __init__(self, base_path=None, **kwargs):
        '''
        Initialize all parameters, using default values if a value is
        not supplied
        '''
		# Initialize all parameters, using default values
        self.base_path = Path.cwd()
		# Initialize boolean options, using default values
        self.parameters_valid = True

        # Update all parameters passed as arguments.
        self.update_parameters(base_path, **kwargs)

    def update_parameters(self, base_path=None, **kwargs):
        '''Update any supplied parameters.
        '''
        if base_path is not None:
            self.update_base_path(base_path)
        # Set boolean options using defined method
        # Boolean options should be set before any corresponding
        # parameters are changed.
        for item in kwargs:
            if hasattr(self, 'set_' + item):
                set_method = getattr(self, 'set_' + item)
                set_method(kwargs[item])
        # Set passed parameters using defined method
        for item in kwargs:
            if hasattr(self, 'update_' + item):
                set_method = getattr(self, 'update_' + item)
                set_method(kwargs[item])

    def insert_base_path(self, file_name: str):
        '''Add the base path to a filename or relative string path.
        Check for presence of ':' or './' as indications that file_name is
            a full or relative path. Otherwise assume that file_name is a
            name or partial path to a file or directory.
        Parameter
            file_name: Type str
                a name or partial path to a file or directory
        Returns
            A full path to a file or directory of type Path
        Raises
            TypeError exception
        '''
        if isinstance(file_name, Path):
            full_path = file_name.resolve()
            return full_path
        elif isinstance(file_name, str):
            if any(a in file_name for a in[':', './']):
                full_path = Path(file_name).resolve()
                return full_path
            else:
                full_path = self.base_path / file_name
                return full_path
        else:
            raise TypeError('file_name must be Type Path or str')

    #The following methods are used to check and update parameters
    def update_base_path(self, directory_path: Path):
        ''' Update the base path.
        directory_path must exist and be a directory.
        directory_path must be of type Path.
        Parameter
            directory_path: Type Path
                The path to be used to complete any file name or partial
                paths
        Raises
            TypeError exception
        '''
        if not isinstance(directory_path, Path):
            raise TypeError('directory_path must be Type Path')
        full_directory_path = self.valid_dir(directory_path)
        self.base_path = full_directory_path

    # The following methods set boolean options to True or False
    def set_parameters_valid(self, is_valid: bool):
        '''Indicate whether the parameters object contains validated
        parameters.
        Parameter
            is_valid: Type bool
                True: Parameters have passed all validation tests.
                False: At least one parameter is not valid.
        Raises
            TypeError
        '''
        try:
            self.parameters_valid = bool(is_valid)
        except TypeError as err:
            raise err('do_scan must be True or False')


class template_selection(ParametersBase):
    '''Contains all parameters required for building Structure Templates.
    Class Attributes:
        base_path (inherited)
            Type: Path
            The starting path to use for incomplete file and directory
            parameters
            Default = Path.cwd()

    Instance Attributes:
        template_directory
            Type: Path
            The path to the directory containing the template files
            Default = base_path / 'Template Spreadsheets'
        template_list_file
            Type: Path
            The path to a excel file containing the information on all current
            templates
            Default =  template_directory / 'Template List.xlsx'
        xml_output_directory
            Type: Path
            The path to the directory where the XML files will be saved.
            Default = base_path / 'Template XML Files'
        selected_templates
            Type: List[str]
            A list of structure template names to be converted to XML.
        status
            Type: String
            Indicates the current stage of the program or any
            error/warning messages
            Default = ""
    Methods
        __init__
			Set attributes
			Verify that attributes are reasonable
        The following methods are used to test or modify passed parameters
            add_base_path(file_name: str)  (inherited)
            is_output_collision()
        The following methods are used to check and update parameters
            update_template_directory(directory_path)
            update_template_list_file(file_path)
            update_xml_output_directory(directory_path)
            update_selected_templates(template_list)
            update_status(status_str)
    '''
    def __init__(self, base_path=None, **kwargs):
        '''
        Initialize all parameters, using default values if a value is
        not supplied
        '''
        # set the base path
        self.update_parameters(base_path)
		# Initialize all parameters using default values
        self.template_directory = self.base_path / 'Template Spreadsheets'
        self.template_list_file = self.template_directory / 'Template List.xlsx'
        self.xml_output_directory = self.base_path / 'Template XML Files'
        self.selected_templates = list()
        self.status = ""
        self.action_text = ''
		# Initialize action methods, using default values
		# FIXME set correct action options
        self.action_methods = dict()
        self.action_sequences = dict()
        self.selected_action = None
        self.run_label = 'Run'
        # Set all passed parameter values
        super().__init__(**kwargs)
        self.template_file_types= FileTypes('Excel Files')

    #The following methods are used to test or modify passed parameters
    def is_output_collision(self):
        '''Check that different templates are not writing to the same file name.
		Not yet implemented
		Returns
            A boolean True if a collision is found.
        '''
        return False

    def update_action_methods(self, actions: dict):
        '''Create a dictionary of callable methods.
        '''
        for (action_name, action_method) in actions:
            if callable(action_method):
                self.action_methods[action_name] = action_method
            else:
                message = 'The method {} for {} is not valid; Ignored'.format(
                    str(action_name), str(action_method))
                raise ParameterWarning(message)

    def valid_action(self, action_name):
        return action_name in self.action_methods

    def update_action_sequences(self, action_sets: dict):
        '''Create a dictionary of callable methods.
        '''
        for (sequence_name, action_sequence) in action_sets:
            if all(self.valid_action(action_name) in self.action_methods):
                self.action_sequence[sequence_name] = action_method
            else:
                message =  'The action {} in sequence {} is not valid.\n'
                message += 'The sequence will be ignored'
                message = message.format(str(action_name), str(action_method))
                raise ParameterWarning(message)

    def update_selected_action(self, action_sequence):
        '''Create a dictionary of callable methods.
        '''
        if action_sequence in self.action_sequences:
            self.selected_action = action_sequence
        else:
            raise ParameterError('% is not a valid action sequence'%action_sequence)

    def set_action_sequence(self):
        '''select the action sequence based on the action options.
        '''
        if self.do_dir_scan:
            if self.parse_dir_data:
                self.update_selected_action('Scan and Parse')
                self.run_label = 'Scan and Parse'
            else:
                self.update_selected_action('Scan and Save')
                self.run_label = 'Scan and Save'
        else:
            self.update_selected_action('Parse File')
            self.run_label = 'Parse File'

    def run(self):
        '''Perform the action sequence
        '''
        action_sequence = self.action_sequences[self.selected_action]
        for action in action_sequence:
            # TODO probably need to add value passing from one action to the next.
            action(self)

    #The following methods are used to check and update parameters
    def update_template_directory(self, directory_path):
        ''' Update the directory containing the template files.
        Parameter
            directory_path: Type Path or str
                The directory path to be scanned.
                If directory_path is a string treat it as a partial and
                combine it with the base path.
                directory_path must exist and be a directory.
        '''
        template_path = self.valid_dir(self.insert_base_path(directory_path))
        self.template_directory = template_path

    def update_template_list_file(self, file_path):
        ''' Update the path to a excel file containing the information on all
        current templates.
        Arguments:
            file_path {str, Path} -- a name or partial path to the excel file
            containing the information on all current templates.
        Raises:
            FileNotFoundError
        '''
        template_file = self.valid_file(self.insert_base_path(file_path))
        if self.template_file_types.check_type:
            self.template_list_file = template_file
        else:
            raise FileTypeError('File for scanning must be and existing Excel file.')

    def update_xml_output_directory(self, directory_path):
        ''' Update the path to the directory where the XML files will be
        saved.
        Arguments:
            directory_path {str, Path} -- a name or partial path to the
            directory where the XML files will be saved.
        Raises
            FileTypeError exception
        '''
        xml_dir = self.valid_dir(self.insert_base_path(directory_path), exist=False)
        self.xml_output_directory = xml_dir

    def update_selected_templates(self, template_names: list[str]):
        ''' Update the list of structure template names to be converted to XML.
        Arguments:
            template_names {List[str]} -- A list of the template names to be
                converted to XML.
        Raises
            ValueError
        '''
        self.selected_templates = template_names

    def update_status(self, status=None):
        '''Update the current program status with current module or
        warning messages.
        Parameter
            status: Type str or Exception
                The current module or an exception.
        '''
        if status:
                self.status = str(status)
        else:
            raise SelectionError('Cannot have Status of "None"')
