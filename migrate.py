import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add GLTFLoader and DRACOLoader
content = content.replace(
    '<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>',
    '<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>\n  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/DRACOLoader.js"></script>\n  <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>'
)

# 2. Add WATCH_FACES to data
watch_faces_str = """    const WATCH_FACES = [
      { id: 'apple', name: 'Apple Watch Ultra', file: 'models/apple_watch_ultra_2.glb', scale: 0.5, px: 0, py: 0, pz: 0, rx: 0, ry: 0, rz: 0 },
      { id: 'rolex', name: 'Rolex', file: 'models/rolex.glb', scale: 1.5, px: 0, py: 0, pz: 0.5, rx: 0, ry: 0, rz: 0 },
      { id: 'ugia', name: 'Ugia Watch', file: 'models/ugia_watch.glb', scale: 0.05, px: 0, py: 0, pz: 0.5, rx: Math.PI/2, ry: 0, rz: 0 }
    ];"""

content = content.replace(
    '    // Trạng thái cấu hình hiện tại',
    watch_faces_str + '\n\n    // Trạng thái cấu hình hiện tại'
)

# 3. Add watchFace to currentConfig
content = content.replace(
    'showWatch: true,',
    'showWatch: true,\n      watchFace: WATCH_FACES[0],'
)

# 4. Replace 3D Engine Variables
vars_old = """    // --- THREE.JS SCENE SETUP ---
    let scene, camera, renderer, controls;
    let strapGroup, watchGroup;
    let shortStrapMesh, longStrapMesh, buckleGroup, stitchMeshes = [];
    let textureLoader;
    let leatherTextures = {};
    let engraveTextureCanvas, engraveTextureContext, engraveTexture;"""

vars_new = """    // --- THREE.JS SCENE SETUP ---
    let scene, camera, renderer, controls;
    let strapModel = null;
    let strapGroup = new THREE.Group();
    let strapMaterials = [];
    let stitchMaterials = [];
    let hardwareMaterials = [];
    let watchGroup = null;
    let loadedWatches = {};
    let textureLoader;
    let leatherTextures = {};
    let leatherNormalMaps = {};
    let currentLeatherColor = new THREE.Color();
    
    let engraveTextureCanvas, engraveTextureContext, engraveTexture;

    const gltfLoader = new THREE.GLTFLoader();
    const dracoLoader = new THREE.DRACOLoader();
    dracoLoader.setDecoderPath('https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/libs/draco/');
    gltfLoader.setDRACOLoader(dracoLoader);"""

content = content.replace(vars_old, vars_new)

# 5. Replace init3D content
# we will replace `buildWatchAndStrap();` inside init3D with the GLTF load logic
build_call = """      // Canvas động cho chữ khắc Laser
      initEngraveCanvas();

      // Dựng cấu trúc hình học 3D hoàn chỉnh
      buildWatchAndStrap();

      // Render loop
      animate();"""

build_call_new = """      // Canvas động cho chữ khắc Laser
      initEngraveCanvas();

      scene.add(strapGroup);

      // Tải mô hình dây da
      gltfLoader.load('models/classic.glb', (gltf) => {
          strapModel = gltf.scene;
          const box = new THREE.Box3().setFromObject(strapModel);
          const center = box.getCenter(new THREE.Vector3());
          strapModel.position.sub(center); 
          strapModel.rotation.z = Math.PI / 2;
          strapModel.rotation.x = Math.PI / 2;
          
          strapGroup.add(strapModel);

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

          update3D();
          if(currentConfig.showWatch) {
              loadWatchFace(currentConfig.watchFace);
          }
      });

      // Render loop
      animate();"""

content = content.replace(build_call, build_call_new)

# 6. Remove old buildWatchAndStrap and createCurvedStrapMesh, createStitching, etc.
# Actually it's easier to just append our new update3D and loadWatchFace functions before animate()
# Let's find animate()
animate_str = """    // Render loop
    function animate() {"""

new_funcs = """
    function loadWatchFace(faceConfig) {
        if(watchGroup) watchGroup.visible = false;
        if(!faceConfig || !currentConfig.showWatch) return;
        
        if(loadedWatches[faceConfig.id]) {
            watchGroup = loadedWatches[faceConfig.id];
            watchGroup.visible = true;
            return;
        }
        
        gltfLoader.load(faceConfig.file, (gltf) => {
            const watchModel = gltf.scene;
            const box = new THREE.Box3().setFromObject(watchModel);
            const center = box.getCenter(new THREE.Vector3());
            watchModel.position.sub(center);
            
            watchModel.scale.set(faceConfig.scale, faceConfig.scale, faceConfig.scale);
            watchModel.position.set(faceConfig.px, faceConfig.py, faceConfig.pz);
            watchModel.rotation.set(faceConfig.rx, faceConfig.ry, faceConfig.rz);
            
            const group = new THREE.Group();
            group.add(watchModel);
            group.position.set(0, 0, 0.4); 
            group.rotation.z = -Math.PI / 2;
            
            scene.add(group);
            loadedWatches[faceConfig.id] = group;
            watchGroup = group;
        });
    }

    function update3D() {
        if (!strapModel) return;

        const tex = textureLoader.load(currentConfig.leather.tex || currentConfig.leather.img);
        const norm = currentConfig.leather.norm ? textureLoader.load(currentConfig.leather.norm) : null;
        tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
        if(norm) norm.wrapS = norm.wrapT = THREE.RepeatWrapping;
        tex.repeat.set(1.5, 1.5);
        if(norm) norm.repeat.set(1.5, 1.5);

        const img = new Image();
        img.src = currentConfig.leather.tex || currentConfig.leather.img;
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
            if(norm) {
                m.normalMap = norm;
                if(m.normalScale) m.normalScale.set(1.2, 1.2);
            }
            m.color.setHex(0xffffff);
            m.roughness = currentConfig.leather.roughness || 0.65;
            m.needsUpdate = true;
        });

        hardwareMaterials.forEach(m => {
            m.color.set(currentConfig.buckleMetal.hex);
            m.metalness = currentConfig.buckleMetal.metalness;
            m.roughness = currentConfig.buckleMetal.roughness;
            m.needsUpdate = true;
        });
    }

    function updateStitch() {
        if (!strapModel) return;
        const sColor = currentConfig.stitch.id === 'matching' ? currentLeatherColor : new THREE.Color(currentConfig.stitch.hex);
        stitchMaterials.forEach(m => {
            m.color = sColor;
            m.needsUpdate = true;
        });
    }
    
    // Render loop
    function animate() {"""

content = content.replace(animate_str, new_funcs)

# Update interaction functions
select_leather_old = """    function selectLeather(leatherId) {
      const item = LEATHER_CATALOG.find(l => l.id === leatherId);
      if (!item) return;
      currentConfig.leather = item;

      // Cập nhật 3D material
      const newMat = createLeatherMaterial(item);
      shortStrapMesh.material = newMat;
      longStrapMesh.material = newMat;

      // Cập nhật UI
      document.getElementById('val-leather').innerText = `${item.name} (${item.color})`;
      document.querySelectorAll('.leather-card').forEach(c => {
        c.classList.toggle('active', c.dataset.id === leatherId);
      });

      updatePrice();
    }"""

select_leather_new = """    function selectLeather(leatherId) {
      const item = LEATHER_CATALOG.find(l => l.id === leatherId);
      if (!item) return;
      currentConfig.leather = item;

      // Cập nhật 3D
      update3D();

      // Cập nhật UI
      document.getElementById('val-leather').innerText = `${item.name} (${item.color})`;
      document.querySelectorAll('.leather-card').forEach(c => {
        c.classList.toggle('active', c.dataset.id === leatherId);
      });

      updatePrice();
    }"""
content = content.replace(select_leather_old, select_leather_new)

select_stitch_old = """    function selectStitch(stitchId) {
      const item = STITCH_COLORS.find(s => s.id === stitchId);
      if (!item) return;
      currentConfig.stitch = item;

      // Nếu là tiệp màu da thì lấy mã hex của da hiện tại
      const hex = item.id === 'matching' ? currentConfig.leather.hex : item.hex;
      stitchMeshes.forEach(mesh => {
        mesh.material.color.set(hex);
      });

      document.getElementById('val-stitch').innerText = item.name;
      document.querySelectorAll('.stitch-swatch').forEach(s => {
        s.classList.toggle('active', s.dataset.id === stitchId);
      });
    }"""

select_stitch_new = """    function selectStitch(stitchId) {
      const item = STITCH_COLORS.find(s => s.id === stitchId);
      if (!item) return;
      currentConfig.stitch = item;

      updateStitch();

      document.getElementById('val-stitch').innerText = item.name;
      document.querySelectorAll('.stitch-swatch').forEach(s => {
        s.classList.toggle('active', s.dataset.id === stitchId);
      });
    }"""
content = content.replace(select_stitch_old, select_stitch_new)


select_buckle_old = """    function selectBuckleMetal(metalId) {
      const item = BUCKLE_METALS.find(m => m.id === metalId);
      if (!item) return;
      currentConfig.buckleMetal = item;

      if (buckleGroup) {
        buckleGroup.traverse(child => {
          if (child.isMesh && child.material && child.geometry.type.includes('Torus') || child.geometry.type.includes('Cylinder')) {
            child.material.color.set(item.hex);
            child.material.metalness = item.metalness;
            child.material.roughness = item.roughness;
          }
        });
      }

      document.getElementById('val-buckle').innerText = `${item.name} (${currentConfig.buckleType === 'tang' ? 'Khóa kim' : 'Khóa bướm'})`;
      document.querySelectorAll('.buckle-card').forEach(b => {
        b.classList.toggle('active', b.dataset.id === metalId);
      });
    }"""

select_buckle_new = """    function selectBuckleMetal(metalId) {
      const item = BUCKLE_METALS.find(m => m.id === metalId);
      if (!item) return;
      currentConfig.buckleMetal = item;

      update3D();

      document.getElementById('val-buckle').innerText = `${item.name} (${currentConfig.buckleType === 'tang' ? 'Khóa kim' : 'Khóa bướm'})`;
      document.querySelectorAll('.buckle-card').forEach(b => {
        b.classList.toggle('active', b.dataset.id === metalId);
      });
    }"""
content = content.replace(select_buckle_old, select_buckle_new)

toggle_watch_old = """    function toggleWatchCase() {
      currentConfig.showWatch = !currentConfig.showWatch;
      watchGroup.visible = currentConfig.showWatch;
      const btn = document.getElementById('btn-toggle-watch');
      btn.innerText = `⌚ Ướm Đồng Hồ: ${currentConfig.showWatch ? 'BẬT' : 'TẮT'}`;
      btn.classList.toggle('active', currentConfig.showWatch);
    }"""

toggle_watch_new = """    function toggleWatchCase() {
      currentConfig.showWatch = !currentConfig.showWatch;
      const btn = document.getElementById('btn-toggle-watch');
      btn.innerText = `⌚ Ướm Đồng Hồ: ${currentConfig.showWatch ? 'BẬT' : 'TẮT'}`;
      btn.classList.toggle('active', currentConfig.showWatch);
      
      if(currentConfig.showWatch) {
          loadWatchFace(currentConfig.watchFace);
      } else if(watchGroup) {
          watchGroup.visible = false;
      }
    }
    
    function setWatchFace(faceId) {
        const face = WATCH_FACES.find(f => f.id === faceId);
        if(!face) return;
        currentConfig.watchFace = face;
        
        document.getElementById('val-watchface').innerText = face.name;
        document.querySelectorAll('.watchface-pill').forEach(p => p.classList.remove('active'));
        event.target.classList.add('active');
        
        if(currentConfig.showWatch) {
            loadWatchFace(face);
        }
    }
    """
content = content.replace(toggle_watch_old, toggle_watch_new)

# Add watch face step to UI
ui_step = """          <div class="step-header">
            <span class="step-title"><span class="step-num">3</span> Khóa & Màu Kim Loại</span>"""

ui_step_new = """          <!-- Watch face toggle -->
          <div class="step-header" style="margin-bottom: 10px;">
            <span class="step-title" style="font-size: 11px;">Mặt đồng hồ ướm thử</span>
            <span class="step-selected-val" id="val-watchface">Apple Watch Ultra</span>
          </div>
          <div class="pill-group" style="margin-bottom: 20px;">
            <div class="size-pill active watchface-pill" onclick="setWatchFace('apple')">Apple</div>
            <div class="size-pill watchface-pill" onclick="setWatchFace('rolex')">Rolex</div>
            <div class="size-pill watchface-pill" onclick="setWatchFace('ugia')">Ugia</div>
          </div>

          <div class="step-header">
            <span class="step-title"><span class="step-num">3</span> Khóa & Màu Kim Loại</span>"""
content = content.replace(ui_step, ui_step_new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("done")
