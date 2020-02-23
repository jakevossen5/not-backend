from flask import Flask, request
from flask import request, jsonify
# from flask_cors import CORS

app = Flask(__name__)
# CORS(app)


@app.route('/')
def start():
    return 'server running'


@app.route('/post', methods=['POST'])
def rec():
    # data = d.json
    print(request.form.get('url'))
    return jsonify(request.form.get('url'))
    # return data['url']


if __name__ == "__main__":
    app.run(debug=True)
