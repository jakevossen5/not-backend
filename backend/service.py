import os
import time
import subprocess
from flask import Flask, request
from flask import request, jsonify, json
from flask_cors import CORS
import wget
import uuid
from typing import List
import requests

app = Flask(__name__)
cors = CORS(app)

uuids_to_paths = {}
current_port_number = 5001


@app.route('/')
def start():
    # handle_request('test', 'test2')
    return 'server running'


@app.route('/r/<uid>/<method>/', methods=['GET', 'OPTIONS'])
def handle_request_no_parms(uid: str, method: str):
    return handle_request(uid, method, "")


@app.route('/r/<uid>/<method>/<parms>', methods=['GET', 'OPTIONS'])
def handle_request(uid: str, method: str, parms: str):
    print('method is', method)
    global current_port_number
    print('in handle request')
    parms = '/'.join(parms.split(','))
    main_path = uuids_to_paths[uid]
    # os.system('nohup python3 test/main.py &')
    print(
        'nohup $(FLASK_APP=' + uuids_to_paths[uid] + ';flask run --host 127.0.0.1 --port ' + str(current_port_number) + ') &')
    os.system(
        'nohup $(FLASK_APP=' + uuids_to_paths[uid] + ';flask run --host 127.0.0.1 --port ' + str(current_port_number) + ') &')

    time.sleep(3)

    r = requests.get('http://127.0.0.1:' +
                     str(current_port_number) + '/' + method + '/' + parms)
    print('responce?', r.text)
    # need to do a request to localhost to call the method that they want

    print('after os system')
    current_port_number += 1
    return jsonify(r.text)


@app.route('/post/<unamerepo>', methods=['POST', 'OPTIONS'])
def rec(unamerepo: str):

    uid = str(uuid.uuid4())

    uname: str = unamerepo.split(',')[0]
    repo: str = unamerepo.split(',')[1]

    # todo - fixup repo formatting if there is an issue

    # example url https://github.com/jakevossen5/jake.vossen.dev/archive/master.zip
    git_url: str = 'https://github.com/' + \
        uname + '/' + repo + '/archive/master.zip'

    uid_dep = uid + '-dep'

    wget.download(git_url)
    download_zip_folder = repo + '-master'
    os.system('unzip ' + download_zip_folder + ' -d ' + uid)
    os.system('unzip ' + download_zip_folder + ' -d ' + uid_dep)
    os.system('rm *.zip')

    # figure out how to output
    in_file_path = uid + '/' + repo + '-master/main.py'
    out_file_path = uid_dep + '/' + repo + '-master/main.py'
    uuids_to_paths[uid] = out_file_path

    # handle_request(uid)

    convert(in_file_path, out_file_path, uid)

    response = app.response_class(
        response=json.dumps(request.form.get('url')),
        status=200,
        mimetype='application/json'
    )

    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    print(request.form.get('url'))
    # return jsonify(unamerepo) this is what jake had i commented out for testing return url
    return jsonify(uid)
    # return data['url']


def convert(input_file: str, output_file: str, uid: str) -> None:

    output_lines: List[str] = []

    output_lines.append("from flask import Flask")
    output_lines.append("app = Flask(__name__)")

    with open(input_file) as f:
        input_file_lines = f.readlines()

    for line in input_file_lines:
        # dealing with a function, we need to add a flask decorator
        if line.startswith('def'):
            decorator: str = get_flask_decorator(line, uid)
            output_lines.append(decorator)
        output_lines.append(line)

    output_lines.append("if __name__ == '__main__':")
    output_lines.append("    app.run(debug=True, host='127.0.0.1')")

    print("printing output lines")

    output_file = open(output_file, 'w')
    for line in output_lines:
        output_file.write(line + '\n' if len(line) > 0 else '')


def get_flask_decorator(line: str, uid: str):
    # should probably do this with a regex but hackathon am i right
    func_name = line.split('(')[0].split(' ')[1]
    # string def func(line: str, uid: str)
    params = line.split('(')[1].split(',')
    params[len(params)-1] = params[len(params)-1][:-3]
    if '' in params:
        params.remove('')
    print('params', params)

    result = ''
    for p in params:
        result += '<'
        result += p.strip()
        result += '>/'
    tail = ','.join(params)
    tail = ''.join([x if x != ' ' else '' for x in tail])
    print(result)
    return "@app.route('/" + func_name + '/' + result + "')"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
