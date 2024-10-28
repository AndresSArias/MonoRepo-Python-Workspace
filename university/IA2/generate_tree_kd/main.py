import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout

def load_data(file_path):
    return pd.read_csv(file_path)

class KDNode:
    def __init__(self, point, left=None, right=None):
        self.point = point
        self.left = left
        self.right = right

def build_kd_tree(points, depth=0):
    if not points:
        return None

    k = len(points[0])
    axis = depth % k
    points.sort(key=lambda x: x[axis])
    median = len(points) // 2

    return KDNode(
        point=points[median],
        left=build_kd_tree(points[:median], depth + 1),
        right=build_kd_tree(points[median + 1:], depth + 1)
    )

# Modificar para imprimir los valores reales de los nodos
def add_edges(graph, node, parent=None, depth=0, label="", node_id=[0], node_values=[]):
    if node is None:
        return

    # Crear un nombre único para cada nodo (usando un índice simple)
    node_label = f"Node{node_id[0]}"
    node_values.append((node_label, node.point))  # Guardar el nodo con su valor real
    node_id[0] += 1

    # Añadir nodo al gráfico
    graph.add_node(node_label)
    if parent:
        graph.add_edge(parent, node_label, label=label)

    # Llamadas recursivas para hijos izquierdo y derecho
    add_edges(graph, node.left, node_label, depth + 1, "L", node_id, node_values)
    add_edges(graph, node.right, node_label, depth + 1, "R", node_id, node_values)

# Función para dibujar el árbol KD y devolver los valores de los nodos
def draw_kd_tree(tree, title="KD Tree"):
    graph = nx.DiGraph()
    node_values = []  # Lista para guardar los valores reales de los nodos
    add_edges(graph, tree, node_values=node_values)

    pos = graphviz_layout(graph, prog="dot")
    plt.figure(figsize=(12, 8))
    nx.draw(graph, pos, with_labels=True, node_color="lightblue", node_size=3000, font_size=10, font_weight="bold", arrows=False)


    # Imprimir los valores reales de cada nodo
    print("\nValores de los nodos en el árbol:")
    for node_label, point in node_values:
        print(f"{node_label}: {point}")
    
    plt.title(title)
    plt.show()

# Función para generar reglas a partir del árbol KD
def generate_rules(node, depth=0, rule_list=[]):
    if node is None:
        return

    k = len(node.point)
    axis = depth % k

    # Modificación para mostrar las reglas en español
    rule_list.append(f"Profundidad {depth}: División en el eje {axis} en {node.point[axis]}")
    
    generate_rules(node.left, depth + 1, rule_list)
    generate_rules(node.right, depth + 1, rule_list)



def main(languaje):
    # Ruta del archivo CSV (específica para tu entorno)
    file_path = "resource/accent-mfcc-data-1.csv"

    # Cargar los datos
    data = load_data(file_path)

    # Crear el árbol KD solo para el lenguaje seleccionado
    lang_data = data[data['language'] == languaje].drop(columns=['language']).values
    tree = build_kd_tree(lang_data.tolist())

    # Generar reglas para el lenguaje seleccionado
    rules = []
    generate_rules(tree, 0, rules)

    # Imprimir las reglas generadas
    print(f"Reglas para {languaje}:")
    for rule in rules[:10]:  # Imprime las primeras 10 reglas
        print(rule)
    print("\n")

    # Dibujar el árbol KD y mostrar los valores de cada nodo
    draw_kd_tree(tree, title=f"KD Tree for {languaje}")


if __name__ == "__main__":
    print("Bienvenido al generador de árboles KD")
    lenguaje_seleccionado = input("Introduce el lenguaje que deseas procesar (ej: ES, FR, GE, IT, UK, US): ").upper()
    main(lenguaje_seleccionado)
    print("Cerrando programa")
