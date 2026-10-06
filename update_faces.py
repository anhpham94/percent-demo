import re

with open('3d.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update UI Elements
html = re.sub(
    r'<div class="step" id="watch-options">.*?</div>\s*</div>\s*<div class="footer">',
    r'''<div class="step" id="watch-options">
                <h3 id="lbl-watchcase">4. ƯỚM THỬ VỚI MẶT ĐỒNG HỒ <span>Apple Watch Ultra</span></h3>
                <div class="grid-3" id="watchface-grid"></div>
            </div>
        </div>
        
        <div class="footer">''',
    html, flags=re.DOTALL
)

# 2. Replace watch data arrays
html = re.sub(
    r'const watchCases = \[.*?\];\s*const watchDials = \[.*?\];',
    r'''const watchFaces = [
            { id: 'none', name: 'Không Mặt (Chỉ Dây)', thumb: 'img/tex_p03.jpg' },
            { id: 'apple', name: 'Apple Watch Ultra', thumb: 'img/tex_p08.jpg' },
            { id: 'rolex', name: 'Mặt Tròn Cổ Điển', thumb: 'img/tex_p05.jpg' }
        ];''',
    html, flags=re.DOTALL
)

# 3. Update state
html = re.sub(
    r'watchCase: watchCases\[0\],\s*watchDial: watchDials\[0\],\s*showWatch: true',
    r'watchFace: watchFaces[1]',
    html
)

# 4. Update UI renderer
html = re.sub(
    r"const wcGrid = document\.getElementById\('watchcase-grid'\);.*?wdGrid\.innerHTML = .*?`\s*;\s*}",
    r'''const wfGrid = document.getElementById('watchface-grid');
            if(wfGrid) {
                wfGrid.innerHTML = watchFaces.map(f => `
                    <div class="card ${state.watchFace.id === f.id ? 'active' : ''}" onclick="selectWatchFace('${f.id}')">
                        <div class="color-dot" style="background: url('${f.thumb}'); background-size: cover;"></div>
                        <div class="card-title">${f.name}</div>
                    </div>
                `).join('');
                document.getElementById('lbl-watchcase').innerHTML = `4. ƯỚM THỬ VỚI MẶT ĐỒNG HỒ <span>${state.watchFace.name}</span>`;
            }
        }''',
    html, flags=re.DOTALL
)

# 5. Replace toggleWatch and selectWatchCase/Dial with selectWatchFace
html = re.sub(
    r'window\.toggleWatch = function.*?window\.selectWatchDial = function.*?}',
    r'''window.selectWatchFace = function(id) {
            state.watchFace = watchFaces.find(f => f.id === id);
            renderUI();
            updateWatchFaceModel();
        };''',
    html, flags=re.DOTALL
)

# 6. Add loadWatchFaceModel
html = html.replace('// --- INIT ---', '''
        let currentWatchFaceModel = null;
        
        function updateWatchFaceModel() {
            if (currentWatchFaceModel) {
                scene.remove(currentWatchFaceModel);
                currentWatchFaceModel = null;
            }
            
            const faceType = state.watchFace.id;
            if (faceType === 'none') return;
            
            let modelPath = '';
            let scale = 1;
            let yOffset = 0;
            
            if (faceType === 'apple') {
                modelPath = 'models/apple_watch_ultra_2.glb';
                scale = 32; // Tweak scale
                yOffset = -0.5;
            } else if (faceType === 'rolex') {
                modelPath = 'models/rolex.glb';
                scale = 450; // Tweak scale
                yOffset = 0;
            }
            
            document.getElementById('loading').style.display = 'flex';
            document.getElementById('loading-text').innerText = 'Đang tải mặt đồng hồ...';
            
            loader.load(modelPath, (gltf) => {
                currentWatchFaceModel = gltf.scene;
                
                // Hide internal straps if they exist in the watch face model
                currentWatchFaceModel.traverse((child) => {
                    if (child.isMesh) {
                        const n = child.name.toLowerCase();
                        if (n.includes('strap') || n.includes('band') || n.includes('clasp')) {
                            child.visible = false;
                        }
                    }
                });
                
                currentWatchFaceModel.scale.set(scale, scale, scale);
                
                // Center it relative to the strap
                const box = new THREE.Box3().setFromObject(currentWatchFaceModel);
                const center = box.getCenter(new THREE.Vector3());
                currentWatchFaceModel.position.x = -center.x;
                currentWatchFaceModel.position.y = -center.y + yOffset;
                currentWatchFaceModel.position.z = -center.z;
                
                // Group it so it matches strap orientation
                const faceGroup = new THREE.Group();
                faceGroup.add(currentWatchFaceModel);
                
                // Rotate to match strap which is upright
                if(faceType === 'apple') {
                    faceGroup.rotation.x = Math.PI / 2;
                    faceGroup.position.y = 10;
                    faceGroup.position.z = 1.5;
                } else if(faceType === 'rolex') {
                    faceGroup.rotation.x = Math.PI / 2;
                    faceGroup.position.y = 10;
                    faceGroup.position.z = 0;
                }
                
                scene.add(faceGroup);
                currentWatchFaceModel = faceGroup; // So it can be removed later
                
                document.getElementById('loading').style.display = 'none';
            });
        }
        
        // --- INIT ---''')

# 7. Add updateWatchFaceModel to initial load
html = html.replace("applyMaterials(strapModel);", "applyMaterials(strapModel);\n                        updateWatchFaceModel();")


with open('3d.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated 3d.html successfully")
