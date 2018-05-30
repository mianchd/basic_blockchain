import hashlib
import json
import time

teststr = 'big brown fox'.encode()
hash_obj = hashlib.sha1(teststr)

class block_chain():
    def __init__(self):

        self.current_transactions = None
        self.chain = []
        
        self.new_block(prev_hash = 1, proof = 599)
    
    def new_block(self, proof, prev_hash=None):

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': prev_hash or self.hash(self.chain[-1]),
            }
        
        self.current_transactions = []
        self.chain.append(block)
        
        return block
    
    def new_transaction(self, sender, recipient, amount):
        new_tx = {
                'sender':sender,
                'receiver':recipient,
                'ammount':amount                
                }
        
        self.current_transactions.append(new_tx)
        return self.last_block['index'] + 1
    
    @property
    def last_block(self):
        return self.chain[-1]
    
    @staticmethod
    def hash(block):
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode() 
        return hashlib.sha256(block_string).hexdigest()
    
    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
