from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
#CORS(app)

@app.route('/')
def start():
    return 'server running'

@app.route('/post/', methods=['POST'])
def rec():
    data = request.json()
    return data['url']

if __name__ == "__main__":
    app.run(debug = True)
