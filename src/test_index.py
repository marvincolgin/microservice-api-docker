from index import app
import unittest
import json


class FlaskAPITests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def tearDown(self):
        pass

    def test_generate_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/generate')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_generate_data(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/generate')

        # Make sure it's a json byte stream
        self.assertIsInstance(result.data, bytes)
        buf = result.data.decode('utf8').replace("'", '"')
        data = json.loads(buf)
        self.assertIsInstance(data, dict)

        # Make sure it has a count field
        c = data.get('count', -1)
        self.assertGreaterEqual(c, 45)

        # Make sure it has a values field
        arr = data.get('values', False)
        self.assertIsNotNone(arr)

        # Make sure the values is []
        self.assertIsInstance(arr, list)

        # Make sure count(values) == data.count
        self.assertEqual(c, len(arr))

    def test_compare_less(self):
        val1 = 1
        val2 = 100
        cs = 1
        result = self.app.get(f'/compare?val1={val1}&val2={val2}&cs={cs}')

        # Make sure it's a json byte stream
        self.assertIsInstance(result.data, bytes)
        buf = result.data.decode('utf8').replace("'", '"')
        data = json.loads(buf)
        self.assertIsInstance(data, dict)

        # Make sure it has 'result:bool'
        r = data.get('result', -1)
        self.assertIsInstance(r, bool)
        self.assertEqual(r, True)

    def test_compare_greater(self):
        val1 = 500
        val2 = 5
        cs = 2
        result = self.app.get(f'/compare?val1={val1}&val2={val2}&cs={cs}')

        # Make sure it's a json byte stream
        self.assertIsInstance(result.data, bytes)
        buf = result.data.decode('utf8').replace("'", '"')
        data = json.loads(buf)
        self.assertIsInstance(data, dict)

        # Make sure it has 'result:bool'
        r = data.get('result', -1)
        self.assertIsInstance(r, bool)
        self.assertEqual(r, True)

    def test_compare_equal(self):
        val1 = 2
        val2 = 2
        cs = 3
        result = self.app.get(f'/compare?val1={val1}&val2={val2}&cs={cs}')

        # Make sure it's a json byte stream
        self.assertIsInstance(result.data, bytes)
        buf = result.data.decode('utf8').replace("'", '"')
        data = json.loads(buf)
        self.assertIsInstance(data, dict)

        # Make sure it has 'result:bool'
        r = data.get('result', -1)
        self.assertIsInstance(r, bool)
        self.assertEqual(r, True)
