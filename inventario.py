import redis

# Conexión a Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Función para agregar un producto al inventario
def agregar_producto(producto_id, nombre, cantidad, precio):
    r.hset(f"producto:{producto_id}", mapping={
        "nombre": nombre,
        "cantidad": cantidad,
        "precio": precio
    })
    print(f"Producto agregado: {nombre}")

# Función para actualizar la cantidad de un producto
def actualizar_cantidad(producto_id, cantidad):
    if r.exists(f"producto:{producto_id}"):
        r.hincrby(f"producto:{producto_id}", "cantidad", cantidad)
        print(f"Cantidad actualizada para el producto {producto_id}")
    else:
        print("El producto no existe")

# Función para consultar la cantidad de un producto
def consultar_cantidad(producto_id):
    if r.exists(f"producto:{producto_id}"):
        cantidad = r.hget(f"producto:{producto_id}", "cantidad")
        nombre = r.hget(f"producto:{producto_id}", "nombre")
        print(f"El producto {nombre.decode('utf-8')} tiene {cantidad.decode('utf-8')} unidades en inventario")
    else:
        print("El producto no existe")

# Función para realizar una venta
def realizar_venta(producto_id, cantidad):
    if r.exists(f"producto:{producto_id}"):
        stock = int(r.hget(f"producto:{producto_id}", "cantidad"))
        if stock >= cantidad:
            r.hincrby(f"producto:{producto_id}", "cantidad", -cantidad)
            print(f"Venta realizada de {cantidad} unidades del producto {producto_id}")
        else:
            print(f"No hay suficiente stock para el producto {producto_id}")
    else:
        print("El producto no existe")

# Ejemplo de uso
agregar_producto(1, "Laptop", 10, 1200.99)
agregar_producto(2, "Smartphone", 20, 599.99)

consultar_cantidad(1)
consultar_cantidad(2)

actualizar_cantidad(1, 5)
consultar_cantidad(1)

realizar_venta(1, 3)
consultar_cantidad(1)
realizar_venta(1, 15)  # Intentar vender más de lo disponible

consultar_cantidad(2)
realizar_venta(2, 5)
consultar_cantidad(2)
