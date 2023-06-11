from hashlib import sha256
import json
import time
import binascii

# following imports are required by PKI
import Cryptodome
import Cryptodome.Random
from Cryptodome.Hash import SHA
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.Cipher import PKCS1_OAEP

class Blockchain:
    def __init__(self):
        self.unconfirmed_transactions = ''
        self.chain = []
        self.transaction = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)
    
    @property
    def last_block(self):
        return self.chain[-1]
    
    difficulty = 2
    def proof_of_work(self, block):
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash
    
    def add_block(self, block, proof, tran):
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        self.transaction.append(tran)
        return True
    
    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())
    
    def add_new_transaction(self, public_key, author, name_book, publisher, genre):
        try:
            new_transaction = Transacion(public_key, author, name_book, publisher, genre)
            print(new_transaction)
            transaction = {
                'Author' : author, 
                'Name Book': name_book,
                'Publisher' : publisher,
                'Genre' : genre
            }
            
            self.unconfirmed_transactions = new_transaction
            return "Success"
        except:
            return "Failed"
    
    def mine(self):
        if self.unconfirmed_transactions == '':
            return False
 
        last_block = self.last_block
 
        new_block = Block(index=last_block.index + 1,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)
 
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof, self.unconfirmed_transactions)
        self.unconfirmed_transactions = []
        return True

class Transacion:
    def __init__(self, public_key, author, name_book, publisher, genre):
        self.public_key = binascii.unhexlify(public_key)
        self.data_author = self.enkripsi(author=author)
        self.data_book = {
            'Name Book': name_book,
            'Publisher' : publisher,
            'Genre' : genre
        }

    def enkripsi(self, author):
        try:
            cipher = PKCS1_OAEP.new(key=RSA.import_key(self.public_key))
            data = cipher.encrypt(message=author.encode('utf-8'))
            print("atas tes")
            return data
        except ValueError as value_error:
            print(value_error)
    
    def get_data_author(self, private_key):
        convert_privateKey = binascii.unhexlify(private_key)
        try:
            cipher = PKCS1_OAEP.new(key=RSA.import_key(convert_privateKey))
            return cipher.decrypt(self.data_author).decode()
        except:
            return "Do not Access"

class Client:
    def __init__(self):
        random = Cryptodome.Random.new().read
        self._private_key = RSA.generate(1024)
        self._public_key = self._private_key.public_key()
        self._signer = PKCS1_v1_5.new(self._private_key)
    
    @property
    def identity(self):
        data = str(self._public_key)
        return binascii.hexlify( data=self._public_key.export_key()).decode('ascii')
    @property
    def identity_private(self):
        return binascii.hexlify( data=self._private_key.export_key()).decode('ascii')
    

class Block:
    def __init__(self, index, timestamp, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()
    
    
    

    
