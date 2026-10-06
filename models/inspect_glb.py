import json
import struct

def inspect_glb(filepath):
    with open(filepath, 'rb') as f:
        magic = f.read(4)
        if magic != b'glTF':
            print(f"Not a GLB file: {filepath}")
            return
        version = struct.unpack('<I', f.read(4))[0]
        length = struct.unpack('<I', f.read(4))[0]
        chunk_len = struct.unpack('<I', f.read(4))[0]
        chunk_type = f.read(4)
        if chunk_type != b'JSON':
            print(f"First chunk is not JSON in {filepath}")
            return
        json_data = f.read(chunk_len).decode('utf-8')
        gltf = json.loads(json_data)
        nodes = gltf.get('nodes', [])
        meshes = gltf.get('meshes', [])
        print(f"--- {filepath} ---")
        for i, node in enumerate(nodes):
            name = node.get('name', f'Node_{i}')
            if 'mesh' in node:
                mesh_idx = node['mesh']
                mesh_name = meshes[mesh_idx].get('name', f'Mesh_{mesh_idx}')
                print(f"  Node {i}: {name} (Mesh: {mesh_name})")
            else:
                pass
                # print(f"  Node {i}: {name}")

inspect_glb('rolex.glb')
inspect_glb('apple_watch_ultra_2.glb')
inspect_glb('ugia_watch.glb')
