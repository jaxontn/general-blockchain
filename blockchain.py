# Module 1 - Create a Blockchain

# To be installed:
# Flask==0.12.2: pip install Flask==0.12.2
# Postman HTTP Client: https://www.getpostman.com/

# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify

# Part 1 - Building a Blockchain

class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0') 
        #the GENESIS block by calling the create_block method


    #NAME: create_block
    #IMPORTS: self, proof, previous_hash
    #EXPORTS: block
    #PURPOSE: CREATING A GENERAL BLOCKCHAIN
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return block



    #NAME: get_previous_block
    #IMPORTS: self (self is the list to all the block)
    #EXPORTS: the last block of the current chain
    #PURPOSE: Just get the last block of the current chain
    def get_previous_block(self):
        return self.chain[-1] #the last index of the chain



    #NAME: proof_of_work
    #IMPORTS: self, previous_proof
    #EXPORTS: new_proof
    #PURPOSE: challenging to solve/find but easy to verify
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000': #the more zeros you put, the harder it is for the miners to mine
                check_proof = True    #miner wins
            else:
                new_proof += 1
        return new_proof
    


    #NAME: hash
    #IMPORTS: self, block
    #EXPORTS: cryptographic hash of the block
    #PURPOSE: take a block and returns the SHA256 of the block
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    


    #NAME: is_chain_valid
    #IMPORTS: self, chain
    #EXPORTS: 
    #PURPOSE: check if the chain is valid
    def is_chain_valid(self, chain):
        previous_block = chain[0] #first block of the chain
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True







# Part 2 - Mining our Blockchain

# Creating a Web App
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Creating a Blockchain
blockchain = Blockchain() #calling the blockchain class we created

# Mining a new block (SOLVING PROOF OF WORK PROBLEM)
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200




# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200





# Checking if the Blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200

# Running the app
app.run(host = '0.0.0.0', port = 5000)
