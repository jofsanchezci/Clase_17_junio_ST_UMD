import redis

# Conectar a Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Establecer una clave-valor
r.set('clave', 'valor')

# Obtener el valor de una clave
valor = r.get('clave')
print(valor.decode('utf-8'))  # 'valor'

# Trabajar con listas
r.rpush('mi_lista', 'elemento1')
r.rpush('mi_lista', 'elemento2')
lista = r.lrange('mi_lista', 0, -1)
print([item.decode('utf-8') for item in lista])  # ['elemento1', 'elemento2']

# Trabajar con hashes
r.hset('mi_hash', 'campo1', 'valor1')
r.hset('mi_hash', 'campo2', 'valor2')
hash_valores = r.hgetall('mi_hash')
print({k.decode('utf-8'): v.decode('utf-8') for k, v in hash_valores.items()})  # {'campo1': 'valor1', 'campo2': 'valor2'}

# Publicar y suscribir a canales
def suscriptor(mensaje):
    print(f"Mensaje recibido: {mensaje['data'].decode('utf-8')}")

pubsub = r.pubsub()
pubsub.subscribe(**{'mi_canal': suscriptor})
pubsub.run_in_thread(sleep_time=0.001)

# Publicar un mensaje
r.publish('mi_canal', 'Hola, Redis!')
