from flask import Flask, render_template, request
import hashlib
from random import sample

#Para subir archivo tipo foto al servidor
from werkzeug.utils import secure_filename 
import os


#Declarando nombre de la aplicación e inicializando
app = Flask(__name__)


#Redireccionando cuando la página no existe
@app.errorhandler(404)
def not_found(error):
    return 'Ruta no encontrada'


def stringAleatorio():
    #Generando string aleatorio
    string_aleatorio = "0123456789abcdefghijklmnopqrstuvwxyz_"
    longitud         = 20
    secuencia        = string_aleatorio.upper()
    resultado_aleatorio  = sample(secuencia, longitud)
    string_aleatorio     = "".join(resultado_aleatorio)
    return string_aleatorio
     
#Creando un Decorador
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/registrar-archivo', methods=['GET', 'POST'])
def registarArchivo():
        if request.method == 'POST':

            #Script para archivo
            file     = request.files['archivo']
            basepath = os.path.dirname (__file__) #La ruta donde se encuentra el archivo actual
            filename = secure_filename(file.filename) #Nombre original del archivo
            
            #capturando extensión del archivo ejemplo: (.png, .jpg, .pdf ...etc)
            extension           = os.path.splitext(filename)[1]
            nuevoNombreFile     = stringAleatorio() + extension
     
            upload_path = os.path.join (basepath, 'static/archivos', nuevoNombreFile)

            file.save(upload_path)


            #Create a Block Class
            class Block:
                #Create a Constructor for the Block class
                def __init__(self,data,prev_hash):
                    self.data = data
                    self.prev_hash = prev_hash
                    self.hash = self.calc_hash()
            
                #Create a method that calculates the hash using SHA-256
                def calc_hash(self):
                    sha = hashlib.sha256()
                    sha.update(self.data.encode('utf-8'))
                    return sha.hexdigest()
            
            #Create the Blockchain Class
            class Blockchain:
                #Create a Constructor for the Blockchain Class
                def __init__(self):
                    self.chain = [self.create_genesis_block()]

                #Create a method that creates the first blockchain also known as the 'Genesis Block'
                def create_genesis_block(self):
                    return Block("Genesis Block", "0")

                #Create a method that creates a new block and adds it to the Blockchain (aka the list)
                def add_block(self,data):
                    prev_block = self.chain[-1]
                    new_block = Block(data,prev_block.hash)
                    self.chain.append(new_block)

            
            #Recorrer archivo cargado
            with  open(upload_path,'r') as file:
                FileBlock = file.read()

            from os import remove
            remove(upload_path)
            

            #Add blocks to the blockchain
            blockchain = Blockchain()
            blockchain.add_block(FileBlock)

            
            #Print and show the blockchain

            for block in blockchain.chain:
                if block.prev_hash == "0":
                    DataG = block.data
                    PreviousG = block.prev_hash
                    HashG = block.hash
                else :
                    Data = block.data
                    Previous = block.prev_hash
                    Hash = block.hash    
      
            
            return "<table border='1'><thead><tr><th>Data</th><th>Previous hash</th><th>Hash</th></tr></thead><tbody><tr><td>" + DataG + "</td><td>" + PreviousG + "</td><td>" + HashG + "</td></tr><tr><td>" + Data + "</td><td>" + Previous + "</td><td>" + Hash + "</td></tr></tbody></table>"
        return render_template('index.html')
    

if __name__ == '__main__':
    app.run(debug=True, port=5000)