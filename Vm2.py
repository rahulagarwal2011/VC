from flask import Flask, jsonify, request
import requests
import json

app = Flask(__name__)
blockchain_chain = []

@app.route('/receive_block', methods=['POST'])
def receive_block():
    global blockchain_chain
    block = request.get_json()
    blockchain_chain.append(block)
    return jsonify({'message': 'Block received and added'}), 200

@app.route('/get_chain', methods=['GET'])
def get_chain():
    return jsonify({'chain': blockchain_chain, 'length': len(blockchain_chain)}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
