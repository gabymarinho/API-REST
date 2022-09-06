# -*- coding: utf-8 -*-

from flask import Flask,request, jsonify
import json
import ast

app = Flask(__name__)
file_name = 'Users.txt'

def read_file(file):
    global read
    with open(file, "r") as file_to_read:
        read = json.load(file_to_read)

def write_file(file):
    global write
    with open(file, "w") as file_to_write:
        json.dump(read, file_to_write, indent=2)

@app.route("/users", methods=['GET'])
def get_users():
   read_file(file_name)
   return jsonify(read)

#usado para analisar uma string JSON válida e convertê-la em um Dicionário Python. 
@app.route("/users", methods=['POST'])
def post_user():
    #Carrega o dado enviado pelo cliente, é convertido em um dicionário python
    data = json.loads(request.data)
    read_file(file_name)
    read.append(data)

    #Criando o arquivo, converto de dicionário python para JSON, e escrevendo os dados anteriores e o atual no arquivo
    write_file(file_name)
    return jsonify(data)

@app.route("/users/<id>", methods=['GET'])
def get_by_id(id):

    read_file(file_name)
    for i in read:
        if str(i['id']) == str(id):
            return jsonify(i)
    return jsonify({'error': 'data not found'})

@app.route("/users/<id>/uppercase", methods=['GET'])
def get_uppercase(id):

    read_file(file_name)
    for i in read:
        if str(i['id']) == str(id):
            convert = str(i)
            #Entende que é um dicionário e converte
            format_json = ast.literal_eval(convert.upper())
            return format_json
    return jsonify({'error': 'data not found'})

@app.route("/users/<id>", methods=['DELETE'])
def delete_user(id):

    read_file(file_name)
        
    for idx, i in enumerate(read):
        if int(i['id']) == int(id):
            read.pop(idx)
    write_file(file_name)
    return "Deleted: {} \n".format(id)

@app.route("/users/<id>", methods=['PATCH'])
def patch_id(id):

    data = json.loads(request.data)
    read_file(file_name)

    for i in read:
        if int(i['id']) == int(id):
            i['username'] = data['username']
    write_file(file_name)
    return "successfully updated"
            