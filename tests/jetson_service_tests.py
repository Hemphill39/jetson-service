import unittest
import welcome

class JetsonServiceTestCase(unittest.TestCase):

    def setUp(self):
        welcome.app.testing = True
        self.app = welcome.app.test_client()

    def tearDown(self):
        print 'tear down'

    def shouldPass(self):
        assert 5 == 5

    def shouldFail(self):
        assert 5 == 6

if __name__ == '__main__':
    unittest.main()