from api import app
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

    def test_generate(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/generate')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

        # Make sure it's a json byte stream
        self.assertIsInstance(result.data, bytes)
        buf = result.data.decode('utf8').replace("'", '"')
        data = json.loads(buf)
        self.assertIsInstance(data, dict)

        # Make sure it has a count field
        c = data.get('count', -1)
        self.assertEqual(c, 10)

        # Make sure it has a values field
        arr = data.get('values', False)
        self.assertIsNotNone(arr)

        # Make sure the values is []
        self.assertIsInstance(arr, list)

        # Make sure count(values) == data.count
        self.assertEqual(c, len(arr))

    def test_public(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

        # Make sure it's a json byte stream
        self.assertIsInstance(result.data, bytes)
        buf = result.data.decode('utf8').replace("'", '"')
        data = json.loads(buf)
        self.assertIsInstance(data, dict)

        # Make sure it's not an ERROR
        err = data.get('error', False)
        self.assertIsNotNone(err, json.dumps(data))

        # Make sure it has a count field
        c = data.get('count', -1)
        self.assertEqual(c, 10)

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

    def test_sort(self):
        data = {'count':5,'values':[{'name':'915','value':1},{'name':'283','value':1},{'name':'350','value':1},{'name':'69','value':1},{'name':'78','value':1}]}  # noqa E231
        result = self.app.post('/sort', data=json.dumps(data), content_type='application/json')

        # Make sure it's a json byte stream
        self.assertIsInstance(result.data, bytes)
        buf = result.data.decode('utf8').replace("'", '"')
        data = json.loads(buf)
        self.assertIsInstance(data, dict)

        expected = {'count':5,'values':['69','78','283','350','915']}  # noqa E231
        self.assertDictEqual(data, expected)
