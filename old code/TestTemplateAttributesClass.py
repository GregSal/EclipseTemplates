import unittest
from TemplateAttributes import *

TemplateAttributesClassTests = unittest.TestSuite()

class Test_TemplateAttribute_creation(unittest.TestCase):
    def test_creation_with_all_parameters(self):
        '''Test create TemplateAttribute instance with all attributes defined'''
        ID = 'TestAttr'
        template_type = 'Structure'
        validate = always_true
        default = 'Default Value'
        test_attr = Variables(ID, template_type, validate, default)
        self.assertEqual(test_attr.ID, ID)
        self.assertEqual(test_attr.template_type, template_type)
        self.assertEqual(test_attr.validate, validate)
        self.assertEqual(test_attr.default, default)

    def test_creation_without_default_parameter(self):
        '''Test create TemplateAttribute instance with only required attributes defined'''
        ID = 'TestAttr'
        template_type = 'Structure'
        validate = always_true
        test_attr = Variables(ID, template_type, validate)
        self.assertEqual(test_attr.ID, ID)
        self.assertEqual(test_attr.template_type, template_type)
        self.assertEqual(test_attr.validate, validate)
        self.assertIsNone(test_attr.default)
        
TemplateAttributesClassTests.addTest(Test_TemplateAttribute_creation('test_creation_without_default_parameter'))
TemplateAttributesClassTests.addTest(Test_TemplateAttribute_creation('test_creation_with_all_parameters'))

#TODO add tests for exceptions raised in TemplateAttribute class
if __name__ == '__main__':
    unittest.main()
