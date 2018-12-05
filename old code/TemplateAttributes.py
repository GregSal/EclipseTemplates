'''Define, Import and Manage Spreadsheet Tables
'''

from pathlib import Path
import re
#import LoggingConfig as log
#logger = log.logging_init(__name__)

class AttributeException(Exception): pass
class InvalidAttribute(AttributeException): pass

always_true = lambda x: True

class Variables(object):
    '''Defines, and validates Attributes for structures and Templates
    
    Attributes
        ID:         Name of XML Attribute or Element Type str 
        Type:       The attribute category.  Can be one of:
                        'Structure'
                        'Template'
		Default:    Default value for the attribute.
                    If None, The attribute value must always be explicitly given.
        validate:   A one variable function that returns a boolean indicating 
                    if the attribute value is valid.  Called in check_values.
                    If not set value checking is not done
    Methods
        __init__
			Set attributes
			Verify that attributes are reasonable
        check_value
            apply validate function(s) to value parameters
        update_default
            if valid, replaces current default with new default value
    Raises
        InvalidAttribute
        '''
    template_types = {'Structure', 'Template'}

    def __init__(self, ID: str, template_type='Structure', validate=always_true, default=None):
        '''Define TemplateAttribute instance, set type, default and validate function
        Parameters
            ID:             Required,   Type str with no spaces
                            Name of XML Attribute or Element Type str 
            template_type:  Required,   Type str
                            The attribute category.  Can be one of:
                                'Structure'
                                'Template'
            validate:       Required,   Type callable
                            A one variable function that returns a boolean indicating 
                            if the attribute value is valid.  Called in check_values.
                            file_path:  Required,   Type Path, 
		    default:        Optional,
                            Default value for the attribute.
                            If None, The attribute value must always be explicitly given.
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

        if isinstance(template_type,str):
            if any(t in template_type for t in self.template_types):
                self.template_type = template_type
            else:
                raise ValueError('template_type must be one of: {}'.format(', '.join(self.template_types)))
        else:
            raise TypeError('template_type must be type str, got type: ' + type(template_type))

        if callable(validate):
            self.validate = validate
        else:
            raise TypeError('validate must be a one variable function that returns a boolean')
            
        if default is None:
            self.default = None
        elif self.validate(default):
            self.default = default


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
            InvalidAttribute
        '''
        if value is None:
            self.default = None
        elif self.validate(value):
            self.default = default
        else:
            raise InvalidAttribute('{} is not a valid attribute for {}'.format(value, self.ID))


if __name__ == '__main__':
    ID = 'TestAttr'
    template_type = 'Structure'
    validate = always_true
    default = None
    test_attr = Variables(ID, template_type, validate, default)
    print(test_attr)
