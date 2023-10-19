from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configuración de la conexión a la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="True1234",
    database="gestion_pedido"
)
cursor = db.cursor(dictionary=True)  # Utiliza dictionary=True para obtener resultados como diccionarios


# Ruta para obtener todos los pedidos
@app.route('/pedidos', methods=['GET'])
def obtener_pedidos():
    cursor.execute("SELECT * FROM pedido")
    pedidos = cursor.fetchall()
    return jsonify(pedidos)


# Ruta para crear un nuevo pedido
@app.route('/pedidos', methods=['POST'])
def crear_pedido():
    data = request.get_json()
    cliente = data['cliente']
    total = data['total']
    estado_pedido = data['estado_pedido']
    fecha_pedido = data['fecha_pedido']

    cursor.execute("INSERT INTO pedido (cliente, total, estado_pedido, fecha_pedido) VALUES (%s, %s, %s, %s)",
                   (cliente, total, estado_pedido, fecha_pedido))
    db.commit()

    # Obtén el ID del pedido recién creado
    cursor.execute("SELECT LAST_INSERT_ID()")
    # noinspection PyTypeChecker
    pedido_id = cursor.fetchone()['LAST_INSERT_ID()']

    return jsonify({'mensaje': 'Pedido creado', 'pedido_id': pedido_id})


# Ruta para obtener un pedido por ID
@app.route('/pedidos/<int:pedido_id>', methods=['GET'])
def obtener_pedido(pedido_id):
    cursor.execute("SELECT * FROM pedido WHERE id = %s", (pedido_id,))
    pedido = cursor.fetchone()
    if pedido:
        return jsonify(pedido)
    return jsonify({'mensaje': 'Pedido no encontrado'}, 404)


# Ruta para actualizar un pedido por ID
@app.route('/pedidos/<int:pedido_id>', methods=['PUT'])
def actualizar_pedido(pedido_id):
    data = request.get_json()
    cliente = data['cliente']
    total = data['total']
    estado_pedido = data['estado_pedido']
    fecha_pedido = data['fecha_pedido']

    cursor.execute("UPDATE pedido SET cliente = %s, total = %s, estado_pedido = %s, fecha_pedido = %s WHERE id = %s",
                   (cliente, total, estado_pedido, fecha_pedido, pedido_id))
    db.commit()
    return jsonify({'mensaje': 'Pedido actualizado'})


# Ruta para eliminar un pedido por ID
@app.route('/pedidos/<int:pedido_id>', methods=['DELETE'])
def eliminar_pedido(pedido_id):
    cursor.execute("DELETE FROM pedido WHERE id = %s", (pedido_id,))
    db.commit()
    return jsonify({'mensaje': 'Pedido eliminado'})


if __name__ == "__main__":
    app.run(debug=True)
