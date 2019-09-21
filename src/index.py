from flask import Flask, request
import sys
import optparse
import time
import requests
from quinnstruct import BinarySearchTree, TraverseMethod, ComparisonSign, HashTable
import json
import random


API_URL = 'https://cf401-finalproject.mcolgin.now.sh/api'


app = Flask(__name__)

start = int(round(time.time()))


def is_json(json_str) -> bool:
    # validate if a string is valid JSON
    try:
        _ = json.loads(json_str)  # noqa UNUSED
    except ValueError:
        return False
    return True


"""
def do_OPTIONS():
    # set options for CORS
    self.send_response(200, "ok")
    self.send_header('Access-Control-Allow-Credentials', 'true')
    self.send_header('Access-Control-Allow-Origin', 'http://localhost:3000')
    self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")
"""


@app.route('/sort', methods=['POST'])
def do_SORT():
    # NO ROUTE, this will take a list of values and sort them, returning the sort via JSON

    arrSortedVals = []

    def touch_node(node):
        # Traversal Routine for BinarySearchTree
        nonlocal arrSortedVals
        arrSortedVals.append(node.value)

    def comparison_func(val1, val2, CS: ComparisonSign):
        # BinarySearchTree function to compare elements
        # DEBUG msg = f'cf() val1:[{val1}] val2:[{val2}] cs:[{CS}]'
        # DEBUG sys.stderr.write(msg.encode())
        if CS == ComparisonSign.EQUAL:
            return int(val1) == int(val2)
        if CS == ComparisonSign.LESS:
            return int(val1) < int(val2)
        if CS == ComparisonSign.GREATER:
            return int(val1) > int(val2)
        return False  # Never get here

    def comparison_api(val1, val2, CS: ComparisonSign):

        if CS == ComparisonSign.EQUAL:
            i = 3
        if CS == ComparisonSign.LESS:
            i = 1
        if CS == ComparisonSign.GREATER:
            i = 2

        # Get Generated Data
        url = f'{API_URL}?cmd=compare&val1={val1}&val2={val2}&cs={i}'
        r = requests.get(url)

        if is_json(r.text):
            data = r.json()

            # Validate Response
            valid = False
            result = data.get('result', None)
            if result is not None:
                valid = True

            if valid:
                return result
            else:
                sys.stderr.write(str(data).encode())
                return False

    # Read in the POST
    body = request.json

    if body is not None and is_json(body):

        # Convert Body to JSON
        obj = json.loads(body)

        # Validate nput
        valid = False
        count = obj.get('count', None)
        if count and count > 0:
            arr = obj.get('values', None)
            if arr and isinstance(arr, list):
                valid = True

        # Create Response
        if valid:

            # Sort using BinarySearchTree
            bt = BinarySearchTree(comparison_api)
            for value in arr:
                bt.add(value.get('name', 'ERROR'))
            bt.traverse(TraverseMethod.IN_ORDER, touch_node)

            # Return Sorted Values
            data = {
                'count': len(arrSortedVals),
                'values': arrSortedVals
            }
            return data
        else:
            # ERROR
            data = {
                'func': 'do_POST',
                'error': f'Invalid Input',
                'body': body
            }
            return data

    else:
        # ERROR
        data = {
            'func': 'do_POST',
            'sub': '!is_json()',
            'error': 'Invalid JSON',
            'payload': f'{body}'
        }
        return data


@app.route('/generate', methods=['GET'])
def do_GENERATE():

    # Generate a Random list of *Unique* Values
    ht = HashTable()
    for _ in range(50):
        x = random.randint(1, 1000)
        if not ht.contains(str(x)):
            ht.add(str(x), 1)

    arrKeys = ht.export_keys()
    values = []
    for x in arrKeys:
        values.append(x)
    data = {
        'count': len(values),
        'values': values,
    }
    return data


@app.route('/compare', methods=['GET'])
def do_COMPARE():
    # Comparison function for BinarySearchTree

    # Validate Input
    val1 = request.args.get('val1')
    val2 = request.args.get('val2')
    cs = request.args.get('cs')
    if val1 is None or val2 is None or cs is None:
        # ERROR
        data = {
            'func': 'do_GET',
            'val1': val1,
            'val2': val2,
            'cs': cs,
            'error': f'Invalid GET params'
        }
        return data

    # Process
    retVal = False
    cs = int(cs)
    if cs == ComparisonSign.EQUAL:
        retVal = val1 == val2
    elif cs == ComparisonSign.LESS:
        retVal = val1 < val2
    elif cs == ComparisonSign.GREATER:
        retVal = val1 > val2

    # Package return
    data = {
        'result': retVal
    }

    # Send Return
    return data


"""
@app.route('/', methods=['GET'])
def do_PUBLIC(self):
    # Sort a List of Random *Unique* Values

    # Get Generated Data
    url = f'{self.API_URL}?cmd=generate'
    r = requests.get(url)

    if self.is_json(r.text):
        data = r.json()

        # Validate Response
        valid = False
        count = data.get('count', None)
        if count and count > 0:
            arr = data.get('values', None)
            if arr and isinstance(arr, list):
                valid = True

        if valid:
            # Pass Data to Sort
            url = f'{self.API_URL}'
            r = requests.post(url, data=json.dumps(data))

            if self.is_json(r.text):
                data = r.json()

                # Validate Response

                # Return Result
                retStr = json.dumps(data)
            else:
                # ERROR
                data = {
                    'func': 'do_GET',
                    'cmd': cmd,
                    'error': f'Invalid JSON',
                    'payload': r.text
                }
                retStr = json.dumps(data)
        else:
            # ERROR
            data = {
                'func': 'do_GET',
                'cmd': cmd,
                'error': f'Invalid Response',
                'payload': str(data)  # this is a dict
            }
            retStr = json.dumps(data)

    else:
        # ERROR
        data = {
            'func': 'do_GET',
            'cmd': cmd,
            'error': 'Invalid JSON',
            'payload': r.text
        }
        retStr = json.dumps(data)

    # Send back to Client
    self.wfile.write(retStr.encode())
    return
"""


if __name__ == "__main__":
    parser = optparse.OptionParser(usage="python simpleapp.py -p ")
    parser.add_option('-p', '--port', action='store', dest='port', help='The port to listen on.')
    (args, _) = parser.parse_args()
    if args.port is None:
        print("Missing required argument: -p/--port")
        sys.exit(1)
    app.run(host='0.0.0.0', port=int(args.port), debug=False)
