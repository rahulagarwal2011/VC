from flask import Flask, jsonify, request
import requests

app = Flask(__name__)
blockchain_data = []

@app.route('/receive_block', methods=['POST'])
def receive_block():
    block = request.get_json()
    blockchain_data.append(block)
    return jsonify({'message': 'Block received'}), 200

@app.route('/get_block', methods=['GET'])
def get_block():
    index = int(request.args.get('index'))
    if 0 < index <= len(blockchain_data):
        return jsonify(blockchain_data[index - 1]), 200
    else:
        return jsonify({'error': 'Invalid block index'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
