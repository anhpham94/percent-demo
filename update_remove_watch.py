import re

with open('3d.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove watch case UI and logic
content = re.sub(r'<div class="option-group">[\s\S]*?<div class="option-title">Vỏ đồng hồ \(Case\)</div>[\s\S]*?</div>', '', content)
content = re.sub(r'<div class="option-group">[\s\S]*?<div class="option-title">Mặt Số \(Watch Face\)</div>[\s\S]*?</div>', '', content)

# 2. Remove procedural watch logic
content = re.sub(r'// --- TẠO MẶT SỐ BẰNG CANVAS ---[\s\S]*?const dialTextures = \{[\s\S]*?\};', '', content)
content = re.sub(r'let watchGroup, watchCaseMaterial, watchDialMaterial;[\s\S]*?// Thêm watchGroup vào scene', '', content)
content = re.sub(r'function createProceduralWatch\(\) \{[\s\S]*?\}', '', content)
content = content.replace("createProceduralWatch();", "")

# 3. Center the strap perfectly!
content = content.replace("// strapModel.position.sub(center); // Bỏ center đi để xem toạ độ gốc", "strapModel.position.sub(center);")
content = content.replace("// strapModel.rotation.z = Math.PI / 2;", "strapModel.rotation.z = Math.PI / 2;")
content = content.replace("// strapModel.rotation.y = Math.PI;", "strapModel.rotation.x = Math.PI / 2;")

# 4. Remove UI event listeners for case and dial
content = re.sub(r'document\.querySelectorAll\(\'#case-options \.option-btn\'\)[\s\S]*?\}\);[\s\S]*?\}\);', '', content)
content = re.sub(r'document\.querySelectorAll\(\'#dial-options \.option-btn\'\)[\s\S]*?\}\);[\s\S]*?\}\);', '', content)

# 5. Fix camera to zoom closely on the leather
content = content.replace("camera.position.set(0, 5, 8);", "camera.position.set(0, 4, 4);")

# 6. Better Lighting for Leather
lighting = """
            scene.add(new THREE.AmbientLight(0xffffff, 0.6));
            
            const dirLight = new THREE.DirectionalLight(0xffffff, 1.0);
            dirLight.position.set(5, 10, 5);
            scene.add(dirLight);

            const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444, 0.8);
            hemiLight.position.set(0, 10, 0);
            scene.add(hemiLight);
            
            const backLight = new THREE.DirectionalLight(0xffffff, 0.5);
            backLight.position.set(-5, -5, -5);
            scene.add(backLight);
"""
content = re.sub(r'scene\.add\(new THREE\.AmbientLight\(0xffffff, 1\.5\)\);[\s\S]*?scene\.add\(dirLight\);', lighting, content)

with open('3d.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated 3d.html")
