from pygltflib import GLTF2
import sys

def print_nodes(gltf, node_idx, level=0):
    node = gltf.nodes[node_idx]
    name = node.name if node.name else f"Node_{node_idx}"
    print("  " * level + f"- {name}")
    if node.children:
        for child_idx in node.children:
            print_nodes(gltf, child_idx, level + 1)

gltf = GLTF2().load(sys.argv[1])
for scene in gltf.scenes:
    for node_idx in scene.nodes:
        print_nodes(gltf, node_idx)
