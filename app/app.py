from flask import Flask, request, jsonify, render_template, redirect, url_for
import redis

# Conexión a Redis
r = redis.Redis(host='localhost', port=6379, db=0)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agregar', methods=['post'])
def agregar_producto():
    producto_id = request.form['producto_id']
    nombre = request.form['nombre']
    cantidad = request.form['cantidad']
    precio = request.form['precio']
    
    r.hset(f"producto:{producto_id}", mapping={
        "nombre": nombre,
        "cantidad": cantidad,
        "precio": precio
    })
    
    return redirect(url_for('index'))

@app.route('/actualizar', methods=['post'])
def actualizar_cantidad():
    producto_id = request.form['producto_id']
    cantidad = int(request.form['cantidad'])
    
    if r.exists(f"producto:{producto_id}"):
        r.hincrby(f"producto:{producto_id}", "cantidad", cantidad)
        return redirect(url_for('index'))
    else:
        return jsonify({"message": "Producto no existe"}), 404

@app.route('/consultar', methods=['post'])
def consultar_cantidad():
    producto_id = request.form['producto_id']
    if r.exists(f"producto:{producto_id}"):
        cantidad = r.hget(f"producto:{producto_id}", "cantidad").decode('utf-8')
        nombre = r.hget(f"producto:{producto_id}", "nombre").decode('utf-8')
        return render_template('index.html', producto=nombre, cantidad=cantidad)
    else:
        return jsonify({"message": "Producto no existe"}), 404

@app.route('/vender', methods=['post'])
def realizar_venta():
    producto_id = request.form['producto_id']
    cantidad = int(request.form['cantidad'])
    
    if r.exists(f"producto:{producto_id}"):
        stock = int(r.hget(f"producto:{producto_id}", "cantidad"))
        if stock >= cantidad:
            r.hincrby(f"producto:{producto_id}", "cantidad", -cantidad)
            return redirect(url_for('index'))
        else:
            return jsonify({"message": "No hay suficiente stock"}), 400
    else:
        return jsonify({"message": "Producto no existe"}), 404

if __name__ == '__main__':
    app.run(debug=True)
