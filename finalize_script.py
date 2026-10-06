import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update WATCH_FACES
new_watches = """
    const WATCH_FACES = [
      { id: 'classic_rolex', name: 'Đồng Hồ Classic Rolex', img: 'img/face_rolex.png' },
      { id: 'smart_apple', name: 'Đồng Hồ Apple Watch', img: 'img/face_apple.png' },
      { id: 'smart_round', name: 'Đồng Hồ Smart Round', img: 'img/face_smart.png' }
    ];
"""
content = re.sub(r'const WATCH_FACES = \[[\s\S]*?\];', new_watches.strip(), content)

# 2. Add buildWatchCase()
watch_dial_logic = """
    let watchDialMaterial = null;
    function buildWatchCase() {
        if(watchGroup) {
            scene.remove(watchGroup);
        }
        watchGroup = new THREE.Group();
        watchGroup.position.set(0, 0, 0.4); 
        watchGroup.rotation.z = -Math.PI / 2;

        const caseMetalMat = new THREE.MeshStandardMaterial({
            color: 0xffffff, metalness: 1.0, roughness: 0.1
        });

        watchDialMaterial = new THREE.MeshPhysicalMaterial({ 
            color: 0xffffff, metalness: 0.1, roughness: 0.5
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
        scene.add(watchGroup);
        watchGroup.visible = currentConfig.showWatch;
    }

    function loadWatchFace(faceConfig) {
        if (!faceConfig || !currentConfig.showWatch) return;
        if (!watchGroup) buildWatchCase();
        
        watchGroup.visible = true;
        textureLoader.load(faceConfig.img, (tex) => {
            tex.colorSpace = THREE.SRGBColorSpace;
            tex.center.set(0.5, 0.5);
            watchDialMaterial.map = tex;
            watchDialMaterial.needsUpdate = true;
        });
    }
"""
content = re.sub(r'function loadWatchFace\(faceConfig\) \{[\s\S]*?\}\n\n', watch_dial_logic + "\n\n", content)

# 3. Add Mobile CSS (Sticky footer + touch targets)
mobile_css = """
      .config-sidebar {
        width: 100vw;
        height: auto;
      }
      .config-scroll {
        padding-bottom: 120px;
      }
      .config-footer {
        position: fixed;
        bottom: 0; left: 0; right: 0;
        z-index: 100;
        border-radius: 20px 20px 0 0;
        padding-bottom: env(safe-area-inset-bottom, 16px);
        box-shadow: 0 -8px 24px rgba(36,24,19,0.1);
      }
      .vp-btn {
        padding: 10px 14px;
        font-size: 13px;
      }
      .size-pill {
        padding: 12px;
      }
      .btn-primary, .btn-secondary {
        padding: 16px;
        font-size: 14px;
      }
"""
content = re.sub(r'\.config-sidebar \{\n\s+width: 100vw;\n\s+height: auto;\n\s+\}', mobile_css.strip(), content)

# 4. Modify HTML pills
watch_html = """
          <div class="pill-group" style="margin-bottom: 20px;">
            <div class="size-pill active watchface-pill" onclick="setWatchFace('classic_rolex', this)">Classic Rolex</div>
            <div class="size-pill watchface-pill" onclick="setWatchFace('smart_apple', this)">Apple Watch</div>
            <div class="size-pill watchface-pill" onclick="setWatchFace('smart_round', this)">Smart Round</div>
          </div>
"""
content = re.sub(r'<div class="pill-group" style="margin-bottom: 20px;">[\s\S]*?</div>', watch_html, content)

# 5. Add Init Watch Call
init_watch_call = """
      // Init Watch Case
      buildWatchCase();
      if(currentConfig.showWatch) {
          loadWatchFace(currentConfig.watchFace);
      }
"""
content = content.replace("update3D();\n    }", "update3D();\n" + init_watch_call + "\n    }")


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Final UI adjustments applied")
