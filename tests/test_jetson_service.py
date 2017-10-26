import unittest
import welcome
from mock import patch
import math

class JetsonServiceTestCase(unittest.TestCase):

    def setUp(self):
        welcome.app.testing = True
        self.app_context = welcome.app.app_context()
        self.app_context.push()
        self.app = welcome.app.test_client()


    def tearDown(self):
        self.app_context.pop()
        print 'tear down'


    def test_shouldPass(self):
        assert 5 == 5


    @patch('welcome.handle_input', return_value='tested query')
    def test_query_watson_should_call_handle_input(self, handle_input_mock):
        self.app.post('/api/query', data=dict(queryText='query', category='washer'))
        handle_input_mock.assert_called_once()


    def test_shouldConfuse(self):
        assert math.sqrt(sum([1,2,3,4,5,6,7,8,9][7:-9:-2][:2],2)) - 4 in set([5,0,1]) ^ set([1,9,4])


if __name__ == '__main__':
    unittest.main()