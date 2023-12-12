from flask import Flask, render_template, request
import hashlib
from random import sample
import os

# Para subir archivo tipo foto al servidor
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt

# Declarando nombre de la aplicación e inicializando
app = Flask(__name__)

# Redireccionando cuando la página no existe
@app.errorhandler(404)
def not_found(error):
    return 'Ruta no encontrada'

def stringAleatorio():
    # Generando string aleatorio
    string_aleatorio = "0123456789abcdefghijklmnopqrstuvwxyz_"
    longitud = 20
    secuencia = string_aleatorio.upper()
    resultado_aleatorio = sample(secuencia, longitud)
    string_aleatorio = "".join(resultado_aleatorio)
    return string_aleatorio

# Creando un Decorador
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/registrar-archivo', methods=['GET', 'POST'])
def registarArchivo():
    if request.method == 'POST':
        # Script para archivo
        file = request.files['archivo']
        basepath = os.path.dirname(__file__)  # La ruta donde se encuentra el archivo actual
        filename = secure_filename(file.filename)  # Nombre original del archivo

        # Capturando extensión del archivo ejemplo: (.png, .jpg, .pdf ...etc)
        extension = os.path.splitext(filename)[1]
        nuevoNombreFile = stringAleatorio() + extension

        upload_path = os.path.join(basepath, 'static/archivos', nuevoNombreFile)
        file.save(upload_path)

        # Create a Block Class
        class Block:
            # Create a Constructor for the Block class
            def __init__(self, data, prev_hash):
                self.data = data
                self.prev_hash = prev_hash
                self.hash = self.calc_hash()

            # Create a method that calculates the hash using SHA-256
            def calc_hash(self):
                sha = hashlib.sha256()
                sha.update(self.data.encode('utf-8'))
                return sha.hexdigest()

        # Create the Blockchain Class
        class Blockchain:
            # Create a Constructor for the Blockchain Class
            def __init__(self):
                self.chain = [self.create_genesis_block()]

            # Create a method that creates the first blockchain also known as the 'Genesis Block'
            def create_genesis_block(self):
                return Block("Genesis Block", "0")

            # Create a method that creates a new block and adds it to the Blockchain (aka the list)
            def add_block(self, data):
                prev_block = self.chain[-1]
                new_block = Block(data, prev_block.hash)
                self.chain.append(new_block)

        # Recorrer archivo cargado
        with open(upload_path, 'r') as file:
            FileBlock = file.read()

        from os import remove
        remove(upload_path)

        # Add blocks to the blockchain
        blockchain = Blockchain()
        VectorFile = FileBlock.split("\n")

        Encabezado = "<table border='1' style='border-collapse: collapse; width: 100%;'><thead><tr style='background-color: gray; color: white;'><th>Data</th><th>Previous hash</th><th>Hash</th></tr></thead><tbody>"
        concatenar = ""

        for item in VectorFile:
            blockchain.add_block(item)

            # Print and show the blockchain
            for block in blockchain.chain:
                Previous = block.prev_hash
                Hash = block.hash

            concatenar = concatenar + "<tr><td>" + item + "</td><td>" + Previous + "</td><td>" + Hash + "</td></tr>"
        
        PiedePagina = "</tbody></table>"

        # Crear un gráfico para visualizar la cadena de bloques
        plt.figure(figsize=(8, 6))

        # Extraer datos para la leyenda
        block_numbers = range(1, len(blockchain.chain) + 1)
        previous_hashes = [block.prev_hash for block in blockchain.chain]
        current_hashes = [block.hash for block in blockchain.chain]

        # Graficar líneas con leyendas
        plt.plot(block_numbers, [int(hash, 16) for hash in previous_hashes], marker='o', linestyle='-', label='Previous Hash', color='blue')
        plt.plot(block_numbers, [int(hash, 16) for hash in current_hashes], marker='o', linestyle='-', label='Current Hash', color='green')

        # Configurar leyendas
        plt.legend()

        # Configurar el resto del gráfico
        plt.title('Blockchain Visualization')
        plt.xlabel('Block Number')
        plt.ylabel('Hash Value (Hexadecimal)')
        plt.grid(True)

        # Guardar el gráfico en un archivo
        graph_path = os.path.join(basepath, 'static', 'graph.png')
        plt.savefig(graph_path)
        plt.close()

        # Texto explicativo
        explicacion_html = """
            <div id="explanation">
                <h2>Entendiendo la Gráfica:</h2>
                <p>
                    Esta gráfica representa la evolución de una cadena de bloques, un tipo especial de registro digital.
                    Cada punto en la línea vertical corresponde a un bloque en la cadena. Los bloques están conectados entre sí
                    mediante la línea azul, indicando la relación cronológica y la seguridad de la cadena.
                </p>
                <p>
                    Los valores hexadecimales en el eje y son las "firmas" únicas (hash) de cada bloque. Estas firmas garantizan
                    la integridad de la información dentro del bloque y aseguran que ningún bloque se altere sin que se note.
                </p>
                <p>
                    Al observar la gráfica, puedes notar cómo la cadena de bloques mantiene una estructura continua, y cualquier cambio
                    en un bloque afectaría a todos los bloques subsiguientes. Esto ilustra la resistencia a la manipulación de la cadena.
                </p>
                <p>
                    En resumen, la cadena de bloques proporciona una forma segura y transparente de almacenar información, donde cada
                    bloque contribuye a la seguridad general de la cadena.
                </p>
            </div>
        """


        # Mostrar la tabla y el gráfico en la página web
        return f"{Encabezado}{concatenar}{PiedePagina}<img src='/static/graph.png' alt='Blockchain Visualization'>{explicacion_html}"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
