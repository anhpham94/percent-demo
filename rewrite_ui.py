import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update WATCH_FACES to use images instead of .glb
new_watches = """
    const WATCH_FACES = [
      { id: 'classic_white', name: 'Đồng Hồ Classic White', img: 'https://images.unsplash.com/photo-1524805444758-089113d48a6d?ixlib=rb-1.2.1&auto=format&fit=crop&w=512&q=80' },
      { id: 'minimal_black', name: 'Đồng Hồ Minimal Black', img: 'https://images.unsplash.com/photo-1523170335258-f5ed11844a49?ixlib=rb-1.2.1&auto=format&fit=crop&w=512&q=80' },
      { id: 'vintage_gold', name: 'Đồng Hồ Vintage Gold', img: 'https://images.unsplash.com/photo-1548169874-531866cb2832?ixlib=rb-1.2.1&auto=format&fit=crop&w=512&q=80' }
    ];
"""
content = re.sub(r'const WATCH_FACES = \[[\s\S]*?\];', new_watches.strip(), content)

# 2. Add procedural watch dial generation logic using textures
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
            tex.center.set(0.5, 0.5);
            watchDialMaterial.map = tex;
            watchDialMaterial.needsUpdate = true;
        });
    }
"""
content = re.sub(r'function loadWatchFace\(faceConfig\) \{[\s\S]*?\}\n\n', watch_dial_logic + "\n\n", content)

# 3. Enhance UI logic to mimic Handdn (Sticky bottom bar)
sticky_footer_css = """
    .configurator-panel {
      width: 400px;
      height: 100%;
      background: var(--pc-cream-card);
      box-shadow: -4px 0 24px rgba(36,24,19,0.06);
      display: flex;
      flex-direction: column;
      z-index: 10;
      position: relative;
    }
    .config-scroll {
      flex: 1;
      overflow-y: auto;
      padding: 32px 24px 100px 24px;
    }
    .sticky-footer {
      position: absolute;
      bottom: 0; left: 0; right: 0;
      background: #fff;
      padding: 16px 24px;
      border-top: 1px solid var(--pc-border);
      box-shadow: 0 -4px 16px rgba(0,0,0,0.05);
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 20;
    }
    .sticky-price {
      font-size: 18px;
      font-weight: 700;
      color: var(--pc-espresso);
    }
    .btn-order {
      background: var(--pc-espresso);
      color: #fff;
      border: none;
      padding: 12px 24px;
      font-size: 14px;
      font-weight: 600;
      letter-spacing: 1px;
      border-radius: 4px;
      cursor: pointer;
      text-transform: uppercase;
      transition: background 0.3s;
    }
    .btn-order:hover {
      background: var(--pc-cognac);
    }
    .step-section {
      margin-bottom: 32px;
      border-bottom: 1px solid var(--pc-border);
      padding-bottom: 24px;
    }
    .step-section:last-child {
      border-bottom: none;
    }
"""
content = re.sub(r'\.configurator-panel \{[\s\S]*?padding: 32px 24px;[\s\S]*?\}', sticky_footer_css, content)

# 4. Inject Sticky Footer HTML
sticky_footer_html = """
      <div class="sticky-footer">
        <div>
          <div style="font-size: 12px; color: var(--pc-text-muted);">Tổng Cộng</div>
          <div class="sticky-price" id="total-price-footer">600,000đ</div>
        </div>
        <button class="btn-order">Thêm Vào Giỏ - Đặt Làm</button>
      </div>
    </div><!-- end configurator-panel -->
"""
content = re.sub(r'</div><!-- end configurator-panel -->', sticky_footer_html, content)

# 5. Modify updatePrice() to update footer
update_price_logic = """
    function updatePrice() {
      const price = currentConfig.leather.price;
      const bucklePrice = (currentConfig.buckleType === 'deployant') ? 150000 : 0;
      const total = price + bucklePrice;
      const formatted = total.toLocaleString('vi-VN') + 'đ';
      
      const priceFooter = document.getElementById('total-price-footer');
      if(priceFooter) priceFooter.innerText = formatted;
    }
"""
content = re.sub(r'function updatePrice\(\) \{[\s\S]*?\}', update_price_logic, content)

# 6. Watch options HTML
watch_html = """
          <div class="pill-group" style="margin-bottom: 20px;">
            <div class="size-pill active watchface-pill" onclick="setWatchFace('classic_white', this)">Classic White</div>
            <div class="size-pill watchface-pill" onclick="setWatchFace('minimal_black', this)">Minimal Black</div>
            <div class="size-pill watchface-pill" onclick="setWatchFace('vintage_gold', this)">Vintage Gold</div>
          </div>
"""
content = re.sub(r'<div class="pill-group" style="margin-bottom: 20px;">[\s\S]*?</div>', watch_html, content)

# 7. Add default watch initialization in init3D
init_watch_call = """
      // Init Watch Case
      buildWatchCase();
      if(currentConfig.showWatch) {
          loadWatchFace(currentConfig.watchFace);
      }
"""
content = content.replace("update3D();", "update3D();\n" + init_watch_call)


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated UI and Watch Faces")
