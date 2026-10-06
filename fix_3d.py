import re

with open('3d.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Hide conflicting meshes
# We want to default to: padding: 'Domed', tip: 'Regular', holes: 'SmallHole'
# We will write a function `updateStrapVisibility()`
vis_func = """
        function updateStrapVisibility() {
            if(!strapModel) return;
            const stylePadding = state.padding || 'Domed';
            const styleTip = state.tip || 'Regular';
            const styleHole = state.hole || 'SmallHole';
            
            strapModel.traverse(child => {
                if(child.isMesh) {
                    const n = child.name;
                    // Nếu là mesh thuộc dây (chứa các từ khóa)
                    if(n.includes('Flat') || n.includes('Square') || n.includes('Domed') || n.includes('Full')) {
                        // Mặc định ẩn
                        let show = false;
                        if (n.includes(stylePadding)) {
                            // Cần check xem nó thuộc Tip hay Hole hay body
                            if (n.includes('Oval') || n.includes('Pilot') || n.includes('Regular') || n.includes('SquareE')) {
                                if (n.includes(styleTip)) show = true;
                            } else if (n.includes('BigHole') || n.includes('SmallHole') || n.includes('Uncut')) {
                                if (n.includes(styleHole)) show = true;
                            } else {
                                show = true; // Các phần body khác (nếu có)
                            }
                        }
                        child.visible = show;
                    }
                }
            });
        }
"""

content = content.replace("function updateStrapMaterial() {", vis_func + "\n        function updateStrapMaterial() {")
content = content.replace("updateStrapMaterial();", "updateStrapVisibility();\n                updateStrapMaterial();")


# 2. Fix Material Assignment - Don't replace the whole material
mat_code = """
                        if (matName === 'DA' || matName === 'LOT') {
                            child.material = child.material.clone();
                            strapMaterials.push(child.material);
                        }
"""
# Find where we set materials
content = re.sub(r'if \(matName === \'DA\' \|\| matName === \'LOT\'\) \{[\s\S]*?\}', mat_code, content)

# Update updateStrapMaterial function
update_mat = """
            strapMaterials.forEach(m => {
                if(m.name === 'DA') {
                    m.map = tex;
                    m.normalMap = norm;
                    if(m.normalScale) m.normalScale.set(1.2, 1.2);
                    m.color.setHex(0xffffff); // Use texture color
                } else if(m.name === 'LOT') {
                    m.color.setHex(0xe8ddc5); // Lining color
                    m.map = null;
                }
                m.needsUpdate = true;
            });
"""
content = re.sub(r'strapMaterials\.forEach\(m => \{[\s\S]*?m\.needsUpdate = true;\n            \}\);', update_mat, content)

# 3. Adjust watchGroup size and position
# caseRadius was 2.0. We should make it 1.0 (diameter 2.0 to match lug width ~2.0)
content = content.replace("const caseRadius = 2.0;", "const caseRadius = 1.0;")
content = content.replace("const caseHeight = 0.5;", "const caseHeight = 0.2;")
content = content.replace("const lugWidth = 1.8;", "const lugWidth = 1.0;")
content = content.replace("const lugLength = 0.8;", "const lugLength = 0.4;")

# 4. Don't center the strap by subtracting its center
# We want to see where it naturally sits. Handdn models might have the watch face at 0,0,0
content = content.replace("strapModel.position.sub(center);", "// strapModel.position.sub(center); // Bỏ center đi để xem toạ độ gốc")

# And disable the rotation for now to see its natural orientation
content = content.replace("strapModel.rotation.z = Math.PI / 2;", "// strapModel.rotation.z = Math.PI / 2;")
content = content.replace("strapModel.rotation.y = Math.PI;", "// strapModel.rotation.y = Math.PI;")

with open('3d.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated 3d.html")
