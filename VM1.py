from flask import Flask, jsonify, request
import datetime
import hashlib
import json
import requests
from threading import Thread

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while not check_proof:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

blockchain = Blockchain()

app = Flask(__name__)

peers = ['http://192.168.1.11:5001', 'http://192.168.1.12:5002']  # Add VM2 and VM3 addresses

@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)

    # Broadcast new block to peers
    Thread(target=broadcast_new_block, args=(block,)).start()

    response = {
        'message': 'Block mined successfully!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200

# Broadcast new block to peers
def broadcast_new_block(block):
    for peer in peers:
        try:
            requests.post(f'{peer}/receive_block', json=block)
        except requests.exceptions.ConnectionError:
            pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
