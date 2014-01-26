import os, sys, six, flask, unittest, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from flask_gacl import gacl, gacl_api, gacl_app

class TestBasics(unittest.TestCase):
    
    def __init__(self, *args, **kwargs): 
        super(TestBasics, self).__init__(*args, **kwargs)
        self.app = gacl_app.app
        self.options = { 
            'debug'             : False,
            'db_uri'            : 'postgresql://gacl:gacl@localhost:5432/gacl_tests',
            'db_name'           : 'gacl_tests',
            'db_table_prefix'   : "",
        }
        self.core = gacl.Gacl(self.options)
        self.api = gacl_api.GaclApi(self.options)
    
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
    
    def test_core(self):
        with self.app.test_request_context():        
            pass


if __name__ == '__main__':
    unittest.main()
