import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace classic.glb loading with buildWatchAndStrap
gltf_load_pattern = r"gltfLoader\.load\('models/classic\.glb'[\s\S]*?\}\);"
build_strap_call = """
      // Dựng dây da 3D bằng mã (Procedural Strap) thay vì dùng mô hình Handdn
      buildWatchAndStrap();
"""
content = re.sub(gltf_load_pattern, build_strap_call, content)

# 2. Add createDialTexture back
canvas_code = """
    // --- TẠO MẶT SỐ BẰNG CANVAS ---
    function createDialTexture(color, style) {
        const canvas = document.createElement('canvas');
        canvas.width = 512;
        canvas.height = 512;
        const ctx = canvas.getContext('2d');
        
        // Nền
        ctx.fillStyle = color;
        ctx.fillRect(0, 0, 512, 512);
        
        ctx.translate(256, 256);
        
        // Vạch số
        ctx.fillStyle = (color === '#ffffff' || color === '#f5f5f5') ? '#333' : '#fff';
        for(let i=0; i<12; i++) {
            ctx.save();
            ctx.rotate((i * 30 * Math.PI) / 180);
            if (style === 'Roman') {
                const numerals = ['XII', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI'];
                ctx.font = 'bold 40px serif';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(numerals[i], 0, -190);
            } else if (style === 'Minimal') {
                ctx.fillRect(-2, -220, 4, 30);
            } else {
                ctx.fillRect(-4, -220, 8, 40);
            }
            ctx.restore();
        }
        
        // Logo
        ctx.font = 'bold 30px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('PERCENT', 0, -80);
        ctx.font = '16px sans-serif';
        ctx.fillText('AUTOMATIC', 0, 100);
        
        const tex = new THREE.CanvasTexture(canvas);
        tex.anisotropy = 16;
        return tex;
    }

    const dialTextures = {
        white_classic: createDialTexture('#f5f5f5', 'Classic'),
        black_minimal: createDialTexture('#222222', 'Minimal'),
        blue_roman: createDialTexture('#1a365d', 'Roman')
    };
"""
# Insert before init3D
content = content.replace("function init3D() {", canvas_code + "\n    function init3D() {")

# 3. Modify buildWatchCase to use Canvas dial and no hands
watch_case_mod = """
      watchDialMaterial = new THREE.MeshPhysicalMaterial({ 
          color: 0xffffff,
          metalness: 0.1,
          roughness: 0.8,
          map: dialTextures.white_classic
      });

      // Vỏ tròn
      const caseGeo = new THREE.CylinderGeometry(3.6, 3.6, 0.9, 48);
      const watchCase = new THREE.Mesh(caseGeo, caseMetalMat);
      watchCase.rotation.x = Math.PI / 2;
      watchCase.castShadow = true;
      watchGroup.add(watchCase);

      // Mặt Dial
      const dialGeo = new THREE.CircleGeometry(3.3, 48);
      const dial = new THREE.Mesh(dialGeo, watchDialMaterial);
      dial.position.z = 0.46;
      watchGroup.add(dial);
      
      // Mặt kính (Kính lồi)
      const glassGeo = new THREE.CylinderGeometry(3.3, 3.3, 0.1, 48);
      const glassMat = new THREE.MeshPhysicalMaterial({
          color: 0xffffff, transmission: 0.95, opacity: 1, transparent: true, roughness: 0, ior: 1.5
      });
      const glass = new THREE.Mesh(glassGeo, glassMat);
      glass.rotation.x = Math.PI / 2;
      glass.position.z = 0.55;
      watchGroup.add(glass);

      // 4 chân Càng Lug
      for (let side of [-1, 1]) {
        for (let end of [-1, 1]) {
          const lugGeo = new THREE.BoxGeometry(0.3, 0.45, 1.1);
          const lug = new THREE.Mesh(lugGeo, caseMetalMat);
          lug.position.set(side * 1.15, 0, end * 3.7);
          watchGroup.add(lug);
        }
      }
"""
content = re.sub(r'const dialGeo = new THREE\.CircleGeometry[\s\S]*?scene\.add\(watchGroup\);\n    \}', watch_case_mod + "\n      scene.add(watchGroup);\n    }", content)


# 4. Remove WATCH_FACES loading logic from setWatchFace
set_watch_face_logic = """
    function setWatchFace(faceId, el) {
      if (el) {
        document.querySelectorAll('#case-options .option-btn').forEach(btn => btn.classList.remove('active'));
        el.classList.add('active');
      }

      if (watchDialMaterial) {
          watchDialMaterial.map = dialTextures[faceId];
          watchDialMaterial.needsUpdate = true;
      }
    }
"""
content = re.sub(r'function setWatchFace\(faceId, el\) \{[\s\S]*?\} // End setWatchFace', set_watch_face_logic + "\n    // End setWatchFace", content)

# 5. Fix UI buttons to pass faceId for Dials
ui_options = """
          <div class="option-list" id="case-options">
            <button class="option-btn active" onclick="setWatchFace('white_classic', this)">Classic White</button>
            <button class="option-btn" onclick="setWatchFace('black_minimal', this)">Minimal Black</button>
            <button class="option-btn" onclick="setWatchFace('blue_roman', this)">Blue Roman</button>
          </div>
"""
content = re.sub(r'<div class="option-list" id="case-options">[\s\S]*?</div>', ui_options, content)
content = content.replace("Vỏ đồng hồ (Case)", "Mặt Số (Dial)")

# Save
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Applied procedural updates")
