from flask import Flask, request, jsonify
import requests
import random

app = Flask(__name__)

# List of VM services
services = {
    'mine_block': 'http://192.168.1.10:5000/mine_block',
    'get_chain': 'http://192.168.1.11:5001/get_chain',
    'get_block': 'http://192.168.1.12:5002/get_block'
}

@app.route('/request/<operation>', methods=['GET'])
def load_balancer(operation):
    if operation == 'mine_block':
        response = requests.get(services['mine_block'])
    elif operation == 'get_chain':
        response = requests.get(services['get_chain'])
    elif operation == 'get_block':
        block_index = request.args.get('index', default=1)
        response = requests.get(f"{services['get_block']}?index={block_index}")
    else:
        return jsonify({'error': 'Invalid operation'}), 400

    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
