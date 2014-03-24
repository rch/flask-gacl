import os, sys, six, flask, unittest, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from flask_gacl import gacl, gacl_api, gacl_app

class TestBasics(unittest.TestCase):
    
    def __init__(self, *args, **kwargs): 
        super(TestBasics, self).__init__(*args, **kwargs)
        self.app = gacl_app.app
        self.options = { 
            'debug'             : True,
            'db_uri'            : 'postgresql://gacl:gacl@localhost:5432/gacl_tests',
            'db_name'           : 'gacl_tests',
            'db_table_prefix'   : "",
        }
        self.core = gacl.Gacl(self.options)
        self.api = gacl_api.GaclApi(self.options)
    
    def _test_core(self):
        with self.app.test_request_context():        
            order = 0
            hidden = 0
            object_type = 'aco'
            # create section
            section_name = 'Default'
            section_value = 'aco-zero'
            object_section_id = self.api.add_object_section(section_name, section_value, order, hidden, object_type)
    
    def test_get_version(self):
        with self.app.test_request_context():
            version = self.api.get_version()
            self.assertTrue(isinstance(version, six.string_types))
            self.assertTrue(isinstance(sum(map(int,version.split('.'))), int))
    
    def test_get_schema_version(self):
        with self.app.test_request_context():
            version = self.api.get_schema_version()
            self.assertTrue(isinstance(version, six.string_types))
            self.assertTrue(isinstance(sum(map(int,version.split('.'))), int))
    
    def test_object_section_ops(self):
        with self.app.test_request_context():
            name = 'ACO Section'
            value = 'aco-section-0'
            order = 0
            hidden = 0
            object_type = 'aco'
            object_section_id = self.api.add_object_section(name, value, order, hidden, object_type)        
            self.api.del_object_section(object_section_id, object_type)
    
    def test_object_ops(self):
        with self.app.test_request_context():
            order = 0
            hidden = 0
            object_type = 'aco'
            # create section
            section_name = 'Default'
            section_value = 'aco-section-zero'
            object_section_id = self.api.add_object_section(section_name, section_value, order, hidden, object_type)
            # create object
            object_value = 'aco-zero'
            object_name = 'BaseACO'
            try:
                self.api.add_object(section_value, object_name, object_value, order, hidden, object_type)
            finally:
                # cleanup
                self.api.del_object_section(object_section_id, object_type)


if __name__ == '__main__':
    unittest.main()
