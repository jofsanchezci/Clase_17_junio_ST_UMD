import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Crear un nuevo gráfico
fig, ax = plt.subplots(figsize=(10, 8))

# Definir los nodos
nodos = {
    "Follower": (1, 2),
    "Candidate": (3, 2),
    "Leader": (5, 2)
}

# Dibujar los nodos
for node, (x, y) in nodos.items():
    ax.add_patch(mpatches.Circle((x, y), 0.3, color='lightblue'))
    ax.text(x, y, node, ha='center', va='center', fontsize=12, fontweight='bold')

# Dibujar las flechas entre los nodos
arrows = [
    ("Follower", "Candidate"),
    ("Candidate", "Leader"),
    ("Leader", "Follower"),
    ("Leader", "Candidate")
]

for start, end in arrows:
    start_x, start_y = nodos[start]
    end_x, end_y = nodos[end]
    ax.annotate('', xy=(end_x, end_y), xytext=(start_x, start_y),
                arrowprops=dict(arrowstyle="->", lw=2))

# Añadir descripciones
descriptions = {
    "Follower": "Escucha heartbeats del líder.\nSe convierte en candidato si no recibe heartbeats.",
    "Candidate": "Incrementa término.\nSolicita votos para ser líder.",
    "Leader": "Envía heartbeats periódicos.\nReplica entradas de log a seguidores."
}

for node, desc in descriptions.items():
    x, y = nodos[node]
    ax.text(x, y-0.6, desc, ha='center', va='top', fontsize=10)

# Ajustar el gráfico
ax.set_xlim(0, 6)
ax.set_ylim(1, 3)
ax.axis('off')

# Título
plt.title("Algoritmo de Consenso para Replicación de Datos (Raft)", fontsize=14)

# Mostrar el gráfico
plt.show()
