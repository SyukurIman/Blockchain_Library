from flask import Flask, request, jsonify
import requests
import json

import blockchain as BS
 
app =  Flask(__name__)

blockchain = BS.Blockchain()

@app.route('/chain', methods=['GET'])
def get_chain():
    data = request.json
    private_key = data['private_key']
    chain_data = []
    for block in blockchain.transaction:
        data = block.get_data_author(private_key)
        print(type(data))
        if block.data_book:
            chain_data.append(["Data Author: "+str(data), "Data Book: "+str(block.data_book)])
        else:
            chain_data.append(["Data Author: "+str(data), 'Data Book: empty'])

    return json.dumps({"length": len(chain_data),
                       "Data ": chain_data})

@app.route('/add_transaksi', methods=['GET'])
def transaction_to():
    data = request.json
    result = blockchain.add_new_transaction(data['public_key'],
                                            data['author'], 
                                            data['name_book'],
                                            data['publisher'],
                                            data['genre'])
    return jsonify({"uuid":result})

@app.route('/mine', methods=['GET'])
def mine_block():
    result = blockchain.mine()
    return jsonify({"uuid":result})

@app.route('/client_register', methods=['GET'])
def client_register():
    client = BS.Client()
    return jsonify({"public_key": client.identity,
                    "private_key": client.identity_private})

app.run(debug=True, port=6060)