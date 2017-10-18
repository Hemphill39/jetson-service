import unittest
import welcome
from mock import patch

class JetsonServiceTestCase(unittest.TestCase):

    mock_cat = [{'class_name': 'water_softener', 'confidence': 0.42}, {'class_name': 'refrigerator', 'confidence': .3}]

    def setUp(self):
        welcome.app.testing = True
        self.app = welcome.app.test_client()

    def tearDown(self):
        print 'tear down'

    def test_shouldPass(self):
        assert 5 == 5

    @patch('welcome.handle_input', return_value="handled")
    def test_query_watson_calls_handle_input(self, handle_input_mock):
        welcome.handle_input('text')
        handle_input_mock.assert_called_once()

    @patch('welcome.nlc', return_value=mock_cat)
    @patch('welcome.discovery.query', return_value='testHtml')
    def test_handle_input_calls_nlc_with_no_user_cat(self, nlc_mock, disc_mock):
        mock_input = {'queryText': 'queryText', 'category': 'user_cat'}
        welcome.handle_input(mock_input)
        nlc_mock.assert_called_once()

    @patch('welcome.nlc', return_value=mock_cat)
    @patch('welcome.discovery.query', return_value='testHtml')
    def test_handle_input_doesnt_call_nlc_if_cat_is_present(self, nlc_mock, disc_mock):
        mock_input = {'queryText': 'queryText', 'category': ''}
        welcome.handle_input(mock_input)

        assert not nlc_mock.called

if __name__ == '__main__':
    unittest.main()