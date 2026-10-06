import re

with open('3d.html', 'r', encoding='utf-8') as f:
    content = f.read()

# We'll completely replace the UI and script sections for cleanliness
new_html = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Percent 3D Bespoke Studio</title>
    <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/DRACOLoader.js"></script>
    <style>
        :root {
            --bg-color: #F6F0E5;
            --text-main: #241813;
            --accent: #9C5A2C;
            --border: #E8DFD0;
            --white: #FFFFFF;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Be Vietnam Pro', sans-serif; }
        body { display: flex; height: 100vh; overflow: hidden; background: var(--bg-color); color: var(--text-main); }
        
        #canvas-container { flex: 1; position: relative; }
        
        #sidebar {
            width: 400px; background: var(--white); border-left: 1px solid var(--border);
            display: flex; flex-direction: column; z-index: 10;
        }
        .header { padding: 20px; border-bottom: 1px solid var(--border); display: flex; align-items: center; gap: 15px; }
        .logo { font-size: 24px; font-weight: 700; background: var(--text-main); color: var(--white); padding: 5px 10px; border-radius: 4px; }
        .title h1 { font-size: 16px; font-weight: 700; letter-spacing: 1px; }
        .title p { font-size: 12px; color: #666; font-style: italic; }
        
        .options-container { flex: 1; overflow-y: auto; padding: 20px; }
        .step { margin-bottom: 30px; }
        .step h3 { font-size: 13px; font-weight: 700; margin-bottom: 15px; text-transform: uppercase; display: flex; justify-content: space-between; }
        .step h3 span { color: var(--accent); font-weight: 600; text-transform: none; }
        
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
        .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
        .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
        
        .card { 
            border: 1px solid var(--border); border-radius: 8px; padding: 10px; text-align: center;
            cursor: pointer; transition: all 0.2s ease; background: #fff;
        }
        .card:hover { border-color: var(--accent); }
        .card.active { border-color: var(--accent); box-shadow: 0 0 0 1px var(--accent); }
        
        .swatch-img { width: 100%; height: 80px; object-fit: cover; border-radius: 4px; margin-bottom: 8px; background: #f0f0f0; }
        .color-dot { width: 30px; height: 30px; border-radius: 50%; margin: 0 auto 8px auto; border: 1px solid #ddd; }
        
        .card-title { font-size: 12px; font-weight: 600; margin-bottom: 4px; }
        .card-price { font-size: 11px; color: var(--accent); }
        
        .footer { padding: 20px; border-top: 1px solid var(--border); background: var(--white); }
        .total-price { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
        .total-price span:first-child { font-size: 14px; font-weight: 600; }
        .total-price span:last-child { font-size: 24px; font-weight: 700; color: var(--text-main); }
        .btn-order { width: 100%; background: var(--text-main); color: var(--white); border: none; padding: 15px; font-size: 14px; font-weight: 700; border-radius: 8px; cursor: pointer; display: flex; justify-content: center; align-items: center; gap: 8px; }
        .btn-order:hover { background: #000; }
        
        /* Camera Controls */
        .camera-controls { position: absolute; top: 20px; left: 20px; display: flex; gap: 10px; z-index: 5; }
        .btn-cam { background: var(--white); border: 1px solid var(--border); padding: 8px 15px; border-radius: 20px; font-size: 12px; font-weight: 600; cursor: pointer; box-shadow: 0 2px 10px rgba(0,0,0,0.05); display: flex; align-items: center; gap: 5px; }
        .btn-cam.active { background: var(--text-main); color: var(--white); border-color: var(--text-main); }
        
        .watch-toggle { position: absolute; top: 20px; right: 20px; display: flex; gap: 10px; z-index: 5; }
        
        #loading { position: absolute; inset: 0; background: var(--bg-color); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 100; transition: opacity 0.5s; }
        .spinner { width: 40px; height: 40px; border: 3px solid rgba(0,0,0,0.1); border-top-color: var(--text-main); border-radius: 50%; animation: spin 1s linear infinite; margin-bottom: 20px; }
        @keyframes spin { to { transform: rotate(360deg); } }
        
        @media (max-width: 900px) {
            body { flex-direction: column; }
            #sidebar { width: 100%; height: 50vh; border-left: none; border-top: 1px solid var(--border); }
            #canvas-container { height: 50vh; }
        }
    </style>
</head>
<body>
    <div id="loading">
        <div class="spinner"></div>
        <div id="loading-text" style="font-weight:600;">Đang nạp 3D Studio... 0%</div>
    </div>

    <div id="canvas-container">
        <div class="camera-controls">
            <button class="btn-cam active" onclick="setCamera('front', this)">🚀 Toàn cảnh</button>
            <button class="btn-cam" onclick="setCamera('top', this)">⬆️ Chụp thẳng</button>
            <button class="btn-cam" onclick="setCamera('side', this)">🔍 Xem độn phồng</button>
        </div>
        <div class="watch-toggle">
            <button class="btn-cam active" id="btn-watch" onclick="toggleWatch()">⌚ Mặt đồng hồ: BẬT</button>
        </div>
    </div>

    <div id="sidebar">
        <div class="header">
            <div class="logo">%</div>
            <div class="title">
                <h1>PERCENT BESPOKE</h1>
                <p>Mô Phỏng 3D Khớp Khối Chuẩn Xác</p>
            </div>
        </div>
        
        <div class="options-container">
            <div class="step">
                <h3 id="lbl-leather">1. CHẤT LIỆU & MÀU DA <span>Agon Soil</span></h3>
                <div class="grid-2" id="leather-grid"></div>
            </div>
            
            <div class="step">
                <h3 id="lbl-stitch">2. CHỈ MAY SADDLE STITCH <span>Tiệp màu</span></h3>
                <div class="grid-4" id="stitch-grid"></div>
            </div>
            
            <div class="step">
                <h3 id="lbl-hardware">3. KHÓA KIM LOẠI <span>Bạc Inox</span></h3>
                <div class="grid-4" id="hardware-grid"></div>
            </div>
            
            <div class="step" id="watch-options">
                <h3 id="lbl-watchcase">4. ƯỚM THỬ VỚI MẶT ĐỒNG HỒ <span>Apple Watch Ultra</span></h3>
                <div class="grid-3" id="watchface-grid"></div>
            </div>
        </div>
        
        <div class="footer">
            <div class="total-price">
                <span>TỔNG CHI PHÍ</span>
                <span id="price-display">650.000₫</span>
            </div>
            <button class="btn-order" onclick="alert('Tính năng đặt hàng đang được cập nhật!')">✨ ĐẶT MAY THỦ CÔNG</button>
        </div>
    </div>

    <script>
        const leathers = [
            { id: 'agon', name: 'Agon', desc: 'Nâu đất Soil', price: 650000, tex: 'img/tex_p01.jpg', norm: 'img/norm_p01.jpg' },
            { id: 'karl', name: 'Karl', desc: 'Nâu Sepia', price: 650000, tex: 'img/tex_p04.jpg', norm: 'img/norm_p04.jpg' },
            { id: 'bruno', name: 'Bruno', desc: 'Vàng bò Gold', price: 650000, tex: 'img/tex_p05.jpg', norm: 'img/norm_p05.jpg' },
            { id: 'cosimo', name: 'Cosimo', desc: 'Xanh Navy Ý', price: 650000, tex: 'img/tex_p08.jpg', norm: 'img/norm_p08.jpg' },
            { id: 'matteo', name: 'Matteo', desc: 'Đỏ rượu Wine', price: 650000, tex: 'img/tex_p10.jpg', norm: 'img/norm_p10.jpg' },
            { id: 'knut', name: 'Knut', desc: 'Đen Cổ Điển', price: 650000, tex: 'img/tex_p03.jpg', norm: 'img/norm_p03.jpg' }
        ];

        const stitches = [
            { id: 'tiep', name: 'Tiệp màu da', color: 'match' },
            { id: 'trang', name: 'Trắng tinh', color: '#ffffff' },
            { id: 'kem', name: 'Kem Vintage', color: '#e8ddc5' },
            { id: 'den', name: 'Đen Tuyền', color: '#111111' },
            { id: 'vang', name: 'Vàng Hermes', color: '#dca654' },
            { id: 'do', name: 'Đỏ Cherry', color: '#b01c1c' }
        ];

        const hardwares = [
            { id: 'silver', name: 'Bạc Inox', color: '#eeeeee', metal: 1, rough: 0.2 },
            { id: 'gold', name: 'Vàng Gold', color: '#d4af37', metal: 1, rough: 0.2 },
            { id: 'rose', name: 'Vàng Hồng', color: '#b76e79', metal: 1, rough: 0.2 },
            { id: 'black', name: 'Đen PVD', color: '#222222', metal: 0.8, rough: 0.4 }
        ];
        
        const watchFaces = [
            { id: 'none', name: 'Không Mặt', thumb: 'img/tex_p03.jpg' },
            { id: 'apple', name: 'Apple Watch Ultra', thumb: 'img/tex_p08.jpg', file: 'models/apple_watch_ultra_2.glb', scale: 0.5, px: 0, py: 0, pz: 0, rx: 0, ry: 0, rz: 0 },
            { id: 'rolex', name: 'Rolex', thumb: 'img/tex_p05.jpg', file: 'models/rolex.glb', scale: 1.5, px: 0, py: 0, pz: 0.5, rx: 0, ry: 0, rz: 0 },
            { id: 'ugia', name: 'Ugia Watch', thumb: 'img/tex_p10.jpg', file: 'models/ugia_watch.glb', scale: 0.05, px: 0, py: 0, pz: 0.5, rx: Math.PI/2, ry: 0, rz: 0 }
        ];

        let state = {
            leather: leathers[0],
            stitch: stitches[0],
            hardware: hardwares[0],
            watchFace: watchFaces[1],
            showWatch: true
        };

        function renderUI() {
            document.getElementById('leather-grid').innerHTML = leathers.map(l => `
                <div class="card ${state.leather.id === l.id ? 'active' : ''}" onclick="selectLeather('${l.id}')">
                    <img src="${l.tex}" class="swatch-img">
                    <div class="card-title">${l.name}</div>
                    <div class="card-price">${l.desc}</div>
                </div>
            `).join('');

            document.getElementById('stitch-grid').innerHTML = stitches.map(s => `
                <div class="card ${state.stitch.id === s.id ? 'active' : ''}" onclick="selectStitch('${s.id}')">
                    <div class="color-dot" style="background: ${s.color === 'match' ? 'linear-gradient(135deg, #444, #999)' : s.color}"></div>
                    <div class="card-title">${s.name}</div>
                </div>
            `).join('');

            document.getElementById('hardware-grid').innerHTML = hardwares.map(h => `
                <div class="card ${state.hardware.id === h.id ? 'active' : ''}" onclick="selectHardware('${h.id}')">
                    <div class="color-dot" style="background: ${h.color}"></div>
                    <div class="card-title">${h.name}</div>
                </div>
            `).join('');
            
            document.getElementById('watchface-grid').innerHTML = watchFaces.map(c => `
                <div class="card ${state.watchFace.id === c.id ? 'active' : ''}" onclick="selectWatchFace('${c.id}')">
                    <div class="card-title">${c.name}</div>
                </div>
            `).join('');

            document.getElementById('lbl-leather').innerHTML = `1. CHẤT LIỆU & MÀU DA <span>${state.leather.name} (${state.leather.desc})</span>`;
            document.getElementById('lbl-stitch').innerHTML = `2. CHỈ MAY SADDLE STITCH <span>${state.stitch.name}</span>`;
            document.getElementById('lbl-hardware').innerHTML = `3. KHÓA KIM LOẠI <span>${state.hardware.name}</span>`;
            document.getElementById('lbl-watchcase').innerHTML = `4. ƯỚM THỬ VỚI MẶT ĐỒNG HỒ <span>${state.watchFace.name}</span>`;
            document.getElementById('price-display').innerText = state.leather.price.toLocaleString('vi-VN') + '₫';
        }

        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xF6F0E5);

        const camera = new THREE.PerspectiveCamera(40, container.clientWidth / container.clientHeight, 0.1, 100);
        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.outputEncoding = THREE.sRGBEncoding;
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 1.2;
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        container.appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.maxDistance = 15;
        controls.minDistance = 2;

        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        scene.add(ambientLight);

        const dirLight = new THREE.DirectionalLight(0xffffff, 1.2);
        dirLight.position.set(5, 8, 5);
        dirLight.castShadow = true;
        scene.add(dirLight);

        const fillLight = new THREE.DirectionalLight(0xd4c5b9, 0.8);
        fillLight.position.set(-5, 3, -5);
        scene.add(fillLight);
        
        const rimLight = new THREE.DirectionalLight(0xffffff, 1.0);
        rimLight.position.set(0, 5, -8);
        scene.add(rimLight);

        let strapModel = null;
        let strapMaterials = [];
        let stitchMaterials = [];
        let hardwareMaterials = [];
        
        let loadedWatches = {};
        let currentWatchGroup = null;

        const textureLoader = new THREE.TextureLoader();
        let currentLeatherColor = new THREE.Color();

        const loader = new THREE.GLTFLoader();
        const dracoLoader = new THREE.DRACOLoader();
        dracoLoader.setDecoderPath('https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/libs/draco/');
        loader.setDRACOLoader(dracoLoader);

        function init3D() {
            loader.load('models/classic.glb', (gltf) => {
                strapModel = gltf.scene;
                
                const box = new THREE.Box3().setFromObject(strapModel);
                const center = box.getCenter(new THREE.Vector3());
                strapModel.position.sub(center); 
                strapModel.rotation.z = Math.PI / 2;
                strapModel.rotation.x = Math.PI / 2;
                
                scene.add(strapModel);

                strapModel.traverse((child) => {
                    if (child.isMesh) {
                        child.castShadow = true;
                        child.receiveShadow = true;
                        const mName = child.name.toLowerCase();
                        if (mName.includes('leather') || mName.includes('padded') || mName.includes('tip') || mName.includes('keeper')) {
                            const newMat = new THREE.MeshStandardMaterial({ roughness: 0.65, metalness: 0.05, color: 0xffffff });
                            child.material = newMat;
                            strapMaterials.push(newMat);
                        } else if (mName.includes('stitch')) {
                            const newMat = new THREE.MeshStandardMaterial({ roughness: 0.9, metalness: 0, color: 0xe8ddc5 });
                            child.material = newMat;
                            stitchMaterials.push(newMat);
                        } else if (mName.includes('buckle') || mName.includes('wire')) {
                            const newMat = new THREE.MeshStandardMaterial({ roughness: 0.2, metalness: 1.0, color: 0xeeeeee });
                            child.material = newMat;
                            hardwareMaterials.push(newMat);
                        }
                    }
                });
                
                document.getElementById('loading').style.opacity = '0';
                setTimeout(() => document.getElementById('loading').style.display = 'none', 500);

                setCamera('front');
                update3D();
                
                // Load default watch face
                if(state.watchFace.file) {
                    loadWatchFace(state.watchFace);
                }

            }, undefined, (err) => {
                console.error(err);
                document.getElementById('loading-text').innerHTML = '<span style="color:red">Lỗi tải mô hình dây đeo</span>';
            });
        }
        
        function loadWatchFace(faceConfig) {
            if(currentWatchGroup) {
                currentWatchGroup.visible = false;
            }
            if(!faceConfig.file || !state.showWatch) {
                return;
            }
            if(loadedWatches[faceConfig.id]) {
                currentWatchGroup = loadedWatches[faceConfig.id];
                currentWatchGroup.visible = true;
                return;
            }
            
            document.getElementById('loading').style.display = 'flex';
            document.getElementById('loading').style.opacity = '1';
            document.getElementById('loading-text').innerText = 'Đang nạp mặt đồng hồ...';
            
            loader.load(faceConfig.file, (gltf) => {
                const watchModel = gltf.scene;
                // Center the watch
                const box = new THREE.Box3().setFromObject(watchModel);
                const center = box.getCenter(new THREE.Vector3());
                watchModel.position.sub(center);
                
                // Apply transformations
                watchModel.scale.set(faceConfig.scale, faceConfig.scale, faceConfig.scale);
                watchModel.position.set(faceConfig.px, faceConfig.py, faceConfig.pz);
                watchModel.rotation.set(faceConfig.rx, faceConfig.ry, faceConfig.rz);
                
                // For UGIA watch which is very small, we might need a different scale, done via faceConfig
                
                const group = new THREE.Group();
                group.add(watchModel);
                
                // Ensure it's correctly aligned with the strap's coordinate system
                // The strap is rotated by Math.PI/2 on X and Z.
                // It's usually placed at the center (0,0,0)
                group.position.set(0, 0, 0.4); 
                group.rotation.z = -Math.PI / 2; // Match strap direction
                
                scene.add(group);
                loadedWatches[faceConfig.id] = group;
                currentWatchGroup = group;
                
                document.getElementById('loading').style.opacity = '0';
                setTimeout(() => document.getElementById('loading').style.display = 'none', 500);
            }, undefined, (err) => {
                console.error(err);
                document.getElementById('loading').style.opacity = '0';
                setTimeout(() => document.getElementById('loading').style.display = 'none', 500);
            });
        }

        function update3D() {
            if (!strapModel) return;

            const tex = textureLoader.load(state.leather.tex);
            const norm = textureLoader.load(state.leather.norm);
            tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
            norm.wrapS = norm.wrapT = THREE.RepeatWrapping;
            tex.repeat.set(1.5, 1.5);
            norm.repeat.set(1.5, 1.5);

            const img = new Image();
            img.src = state.leather.tex;
            img.onload = () => {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                canvas.width = img.width; canvas.height = img.height;
                ctx.drawImage(img, 0, 0);
                const data = ctx.getImageData(0,0,img.width,img.height).data;
                let r=0, g=0, b=0;
                for(let i=0; i<data.length; i+=4){ r+=data[i]; g+=data[i+1]; b+=data[i+2]; }
                const cnt = data.length/4;
                currentLeatherColor.setRGB(r/cnt/255, g/cnt/255, b/cnt/255);
                updateStitch();
            };

            strapMaterials.forEach(m => {
                m.map = tex;
                m.normalMap = norm;
                if(m.normalScale) m.normalScale.set(1.2, 1.2);
                m.color.setHex(0xffffff);
                m.needsUpdate = true;
            });

            hardwareMaterials.forEach(m => {
                m.color.set(state.hardware.color);
                m.metalness = state.hardware.metal;
                m.roughness = state.hardware.rough;
                m.needsUpdate = true;
            });
        }

        function updateStitch() {
            if (!strapModel) return;
            const sColor = state.stitch.color === 'match' ? currentLeatherColor : new THREE.Color(state.stitch.color);
            stitchMaterials.forEach(m => {
                m.color = sColor;
                m.needsUpdate = true;
            });
        }

        function toggleWatch() {
            state.showWatch = !state.showWatch;
            document.getElementById('btn-watch').innerText = state.showWatch ? '⌚ Mặt đồng hồ: BẬT' : '⌚ Mặt đồng hồ: TẮT';
            document.getElementById('watch-options').style.display = state.showWatch ? 'block' : 'none';
            if(state.showWatch) {
                loadWatchFace(state.watchFace);
            } else if(currentWatchGroup) {
                currentWatchGroup.visible = false;
            }
        }

        function setCamera(view, btn) {
            document.querySelectorAll('.btn-cam').forEach(b => b.classList.remove('active'));
            if (btn) btn.classList.add('active');
            else document.querySelector('.btn-cam').classList.add('active');

            const dur = 1000;
            const startPos = camera.position.clone();
            let targetPos = new THREE.Vector3();
            let targetLook = new THREE.Vector3(0,0,0);

            if (view === 'front') { targetPos.set(-4, 5, 8); }
            if (view === 'top') { targetPos.set(0, 10, 0); }
            if (view === 'side') { targetPos.set(7, 2, 2); targetLook.set(3, 0, 0); }

            const startT = performance.now();
            function anim() {
                const now = performance.now();
                const t = Math.min((now - startT) / dur, 1);
                const e = 1 - Math.pow(1 - t, 3);
                camera.position.lerpVectors(startPos, targetPos, e);
                controls.target.lerpVectors(controls.target, targetLook, e);
                if (t < 1) requestAnimationFrame(anim);
            }
            anim();
        }

        window.addEventListener('resize', () => {
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
        });

        function animate() {
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        }

        function selectLeather(id) { state.leather = leathers.find(l => l.id === id); renderUI(); update3D(); }
        function selectStitch(id) { state.stitch = stitches.find(s => s.id === id); renderUI(); updateStitch(); }
        function selectHardware(id) { state.hardware = hardwares.find(h => h.id === id); renderUI(); update3D(); }
        function selectWatchFace(id) { 
            state.watchFace = watchFaces.find(c => c.id === id); 
            renderUI(); 
            if(state.showWatch) loadWatchFace(state.watchFace); 
        }

        renderUI();
        init3D();
        animate();
    </script>
</body>
</html>
"""

with open('3d.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Updated 3d.html successfully")
