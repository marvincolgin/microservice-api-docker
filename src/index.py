from flask import request, jsonify
from factory import create_app
import sys
import optparse
import time
import requests
from quinnstruct import BinarySearchTree, TraverseMethod, ComparisonSign, HashTable
import json
import random


API_URL_BASE = 'http://127.0.0.1:8000'
API_URL_GENERATE = API_URL_BASE + '/generate'
API_URL_SORT = API_URL_BASE + '/sort'
API_URL_COMPARE = API_URL_BASE + '/compare'


API_GENERATE_NUMBER = 10


app = create_app()
start = int(round(time.time()))


def is_json(json_str) -> bool:

    # validate if a string is valid JSON
    try:
        _ = json.loads(json_str)  # noqa UNUSED
    except ValueError:
        return False
    return True


@app.route('/sort', methods=['POST'])
def do_SORT():
    method_name = 'do_SORT'

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
        url = f'{API_URL_COMPARE}?val1={val1}&val2={val2}&cs={i}'
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
    # @TODO: Why do I need to do this? request.json==None when I tried it (content-type from sub req)
    buf = request.data.decode('utf8').replace("'", '"')
    body = json.loads(buf)
    if body is not None:

        # Convert Body to JSON
        if isinstance(body, dict):
            obj = body
        else:
            if is_json(body):
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
            use_web = True
            f = comparison_api if use_web else comparison_func
            bt = BinarySearchTree(f)
            for value in arr:
                bt.add(value.get('name', 'ERROR'))
            bt.traverse(TraverseMethod.IN_ORDER, touch_node)

            # Return Sorted Values
            data = {
                'count': len(arrSortedVals),
                'values': arrSortedVals
            }
            return jsonify(data)
        else:
            # ERROR
            data = {
                'error': f'Invalid Input',
                'method_name': method_name,
                'body': body
            }
            return jsonify(data)

    else:
        # ERROR
        data = {
            'sub': '!is_json()',
            'method_name': method_name,
            'error': 'Invalid JSON',
            'payload': f'{body}'
        }
        return jsonify(data)


@app.route('/generate', methods=['GET'])
def do_GENERATE():
    # method_name = 'do_GENERATE'

    # Generate a Random list of *Unique* Values
    ht = HashTable()
    c = 0
    while c < API_GENERATE_NUMBER:
        x = random.randint(1, 1000)
        if not ht.contains(str(x)):
            ht.add(str(x), 1)
            c += 1

    arrKeys = ht.export_keys()
    values = []
    for x in arrKeys:
        values.append(x)
    data = {
        'count': len(values),
        'values': values,
    }
    return jsonify(data)


@app.route('/compare', methods=['GET'])
def do_COMPARE():
    method_name = 'do_COMPARE'

    # Comparison function for BinarySearchTree

    # Validate Input
    val1 = int(request.args.get('val1'))
    val2 = int(request.args.get('val2'))
    cs = int(request.args.get('cs'))
    if val1 is None or val2 is None or cs is None:
        # ERROR
        data = {
            'val1': val1,
            'val2': val2,
            'cs': cs,
            'method_name': method_name,
            'error': f'Invalid GET params'
        }
        return jsonify(data)

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
    return jsonify(data)


@app.route('/', methods=['GET'])
def do_PUBLIC():
    method_name = 'do_PUBLIC'
    # Sort a List of Random *Unique* Values

    # Get Generated Data
    url = f'{API_URL_GENERATE}'
    r = requests.get(url)

    if r is not None and is_json(r.text):
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
            url = f'{API_URL_SORT}'
            r = requests.post(url, data=json.dumps(data))

            if is_json(r.text):
                data = r.json()

                # Validate Response

                # Return Result
                return jsonify(data)
            else:
                # ERROR
                data = {
                    'method_name': method_name,
                    'url': url,
                    'error': f'Invalid JSON',
                    'payload': r.text
                }
                return jsonify(data)
        else:
            # ERROR
            data = {
                'method_name': method_name,
                'note': 'count from json didn''t match values[]',
                'error': f'Invalid Response',
                'payload': str(data)  # this is a dict
            }
            return jsonify(data)

    else:
        # ERROR
        data = {
            'method_name': method_name,
            'url': url,
            'error': 'Invalid JSON',
            'payload': r.text
        }
        return jsonify(data)

    # Send back to Client
    return jsonify({
        'method_name': method_name,
        'error': f'ASSERT! This should never get here'
    })


if __name__ == "__main__":
    parser = optparse.OptionParser(usage="python " + __name__ + " -p ")
    parser.add_option('-p', '--port', action='store', dest='port', help='The port to listen on.')
    (args, _) = parser.parse_args()
    if args.port is None:
        print("Missing required argument: -p/--port")
        sys.exit(1)
    app.run(host='0.0.0.0', port=int(args.port), debug=False)
