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

        self.assertIsInstance(result.data, bytes)

        buf = result.data.decode('utf8').replace("'", '"')
        data = json.loads(buf)

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
