import os
import subprocess
from flask import Flask, request
from flask import request, jsonify, json
from flask_cors import CORS
import wget
import uuid
from typing import List

app = Flask(__name__)
cors = CORS(app)


@app.route('/')
def start():
    handle_request('test', 'test2')
    return 'server running'


def handle_request(uid_deployed: str, method: str):
    print('in handle request')
    dir_of_main = '6c501795-2c5e-44a0-b375-2a3115ed1d7f'
    os.system('nohup python3 test/main.py &')
    os.system('export FLASK_APP=test/main.py;flask run --host 127.0.0.1 --port 5001')
    # exec('test/main.py')
    # subprocess.call(
    # ["exec", "mistakes.sh", "test"])


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

    # wget.download(git_url)
    #download_zip_folder = repo + '-master'
    #os.system('unzip ' + download_zip_folder + ' -d ' + uid)
    #os.system('unzip ' + download_zip_folder + ' -d ' + uid_dep)
    # os.system('mv ' + )

    # figure out how to output
    in_file_path = uid + '/' + repo + '-master/main.py'
    out_file_path = uid_dep + '/' + repo + '-master/main.py'

    handle_request('a', 'b')

    # convert(in_file_path, out_file_path, uid)

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
    return jsonify(unamerepo)
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
    output_lines.append("    app.run(debug=True, host='127.0.0.1', port=5001)")

    print("printing output lines")

    output_file = open(output_file, 'wb')
    for line in output_lines:
        output_file.write(line + '\n' if len(line) > 0 else '')


def get_flask_decorator(line: str, uid: str):
    # should probably do this with a regex but hackathon am i right
    func_name = line.split('(')[0].split(' ')[1]
    return "@app.route('/" + uid + '/' + func_name + "')"


if __name__ == "__main__":
    app.run(debug=True)
