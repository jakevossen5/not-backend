from flask import Flask, request
from flask import request, jsonify, json
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)


@app.route('/')
def start():
    return 'server running'


@app.route('/post/<unamerepo>', methods=['POST', 'OPTIONS'])
def rec(unamerepo):
    # data = d.json
    print(unamerepo)
    # data = print('url', request.form.get('url'))
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


if __name__ == "__main__":
    app.run(debug=True)
