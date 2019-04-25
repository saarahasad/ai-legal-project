from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import classification

app = Flask(__name__)
CORS(app)


@app.route('/case-category')
def case_category():
    return jsonify({'data':classification.main_func()})

if __name__ == '__main__':
   app.run(debug = True)

