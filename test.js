  <script>
    // --- DATABASE SẢN PHẨM PERCENT CÓ SẴN (TEXTURE & NORMAL MAP TỰ ĐỘNG BÓC TÁCH TỪ ẢNH THẬT) ---
    const LEATHER_CATALOG = [
      { id: 'agon-soil', name: 'Percent Agon', color: 'Nâu đất Soil', price: 600000, img: 'img/p01.jpg', tex: 'img/tex_p01.jpg', norm: 'img/norm_p01.jpg', hex: '#634E3F', roughness: 0.55 },
      { id: 'karl-sepia', name: 'Percent Karl', color: 'Nâu hạt dẻ Sepia', price: 580000, img: 'img/p04.jpg', tex: 'img/tex_p04.jpg', norm: 'img/norm_p04.jpg', hex: '#5E4842', roughness: 0.50 },
      { id: 'bruno-gold', name: 'Percent Bruno', color: 'Vàng bò Gold', price: 580000, img: 'img/p05.jpg', tex: 'img/tex_p05.jpg', norm: 'img/norm_p05.jpg', hex: '#876527', roughness: 0.60 },
      { id: 'cosimo-navy', name: 'Percent Cosimo', color: 'Xanh Navy Ý', price: 580000, img: 'img/p08.jpg', tex: 'img/tex_p08.jpg', norm: 'img/norm_p08.jpg', hex: '#1C252B', roughness: 0.45 },
      { id: 'matteo-wine', name: 'Percent Matteo', color: 'Đỏ rượu Wine Red', price: 580000, img: 'img/p10.jpg', tex: 'img/tex_p10.jpg', norm: 'img/norm_p10.jpg', hex: '#522421', roughness: 0.50 },
      { id: 'knut-black', name: 'Percent Knut', color: 'Đen Cổ Điển', price: 520000, img: 'img/p03.jpg', tex: 'img/tex_p03.jpg', norm: 'img/norm_p03.jpg', hex: '#2A2C2B', roughness: 0.55 },
    ];

    const STITCH_COLORS = [
      { id: 'cream', name: 'Chỉ kem vintage', hex: '#EBE2D3' },
      { id: 'matching', name: 'Chỉ tiệp màu da', hex: '#442f29' },
      { id: 'white', name: 'Chỉ trắng thanh lịch', hex: '#FFFFFF' },
      { id: 'black', name: 'Chỉ đen mạnh mẽ', hex: '#1C1C1C' },
      { id: 'gold', name: 'Chỉ vàng bò', hex: '#D29B4A' }
    ];

    const BUCKLE_METALS = [
      { id: 'silver', name: 'Bạc Inox', hex: '#D8D8D8', metalness: 0.95, roughness: 0.15 },
      { id: 'gold', name: 'Vàng Gold', hex: '#E5B864', metalness: 0.95, roughness: 0.15 },
      { id: 'rosegold', name: 'Vàng Hồng', hex: '#E2A995', metalness: 0.92, roughness: 0.18 },
      { id: 'black', name: 'Đen PVD', hex: '#242424', metalness: 0.85, roughness: 0.25 }
    ];

    const WATCH_FACES = [
      { id: 'apple', name: 'Apple Watch Ultra', file: 'models/apple_watch_ultra_2.glb', scale: 0.5, px: 0, py: 0, pz: 0, rx: 0, ry: 0, rz: 0 },
      { id: 'rolex', name: 'Rolex', file: 'models/rolex.glb', scale: 1.5, px: 0, py: 0, pz: 0.5, rx: 0, ry: 0, rz: 0 },
      { id: 'ugia', name: 'Ugia Watch', file: 'models/ugia_watch.glb', scale: 0.05, px: 0, py: 0, pz: 0.5, rx: Math.PI/2, ry: 0, rz: 0 },
      { id: 'chronograph', name: 'Chronograph (Khronos)', file: 'models/ChronographWatch.glb', scale: 0.25, px: 0, py: 0, pz: 0.5, rx: Math.PI/2, ry: 0, rz: 0 }
    ];

    // Trạng thái cấu hình hiện tại
    const currentConfig = {
      leather: LEATHER_CATALOG[0],
      stitch: STITCH_COLORS[0],
      buckleMetal: BUCKLE_METALS[0],
      buckleType: 'tang', // tang or deployant
      lugSize: '20 - 18 mm',
      wristSize: '16.5 cm (Chuẩn 115/75mm)',
      engraving: '',
      showWatch: true,
      watchFace: WATCH_FACES[0],
      autoRotate: true
    };

    // --- THREE.JS SCENE SETUP ---
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
    gltfLoader.setDRACOLoader(dracoLoader);

    
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

    function init3D() {
      const container = document.querySelector('.viewport-container');
      const canvas = document.getElementById('webgl-canvas');

      scene = new THREE.Scene();
      scene.background = null;

      camera = new THREE.PerspectiveCamera(40, container.clientWidth / container.clientHeight, 0.1, 1000);
      camera.position.set(0, 18, 28);

      renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true, preserveDrawingBuffer: true });
      renderer.setSize(container.clientWidth, container.clientHeight);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      renderer.toneMappingExposure = 1.25;
      renderer.shadowMap.enabled = true;
      renderer.shadowMap.type = THREE.PCFSoftShadowMap;

      controls = new THREE.OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.05;
      controls.maxDistance = 55;
      controls.minDistance = 12;
      controls.autoRotate = true;
      controls.autoRotateSpeed = 2.0;
      controls.maxPolarAngle = Math.PI / 2 + 0.1;
      controls.target.set(0, 0, 0);

      // --- STUDIO LIGHTING SYSTEM ---
      const ambientLight = new THREE.AmbientLight(0xfff8f0, 0.9);
      scene.add(ambientLight);

      const keyLight = new THREE.DirectionalLight(0xffffff, 1.3);
      keyLight.position.set(15, 25, 20);
      keyLight.castShadow = true;
      keyLight.shadow.mapSize.width = 2048;
      keyLight.shadow.mapSize.height = 2048;
      scene.add(keyLight);

      const fillLight = new THREE.DirectionalLight(0xf5ebe0, 0.8);
      fillLight.position.set(-20, 15, -15);
      scene.add(fillLight);

      const rimLight = new THREE.DirectionalLight(0xfff0dd, 0.6);
      rimLight.position.set(0, -10, 15);
      scene.add(rimLight);

      // Sàn bóng đổ mờ ảo
      const floorGeo = new THREE.PlaneGeometry(100, 100);
      const floorMat = new THREE.ShadowMaterial({ opacity: 0.15 });
      const floor = new THREE.Mesh(floorGeo, floorMat);
      floor.rotation.x = -Math.PI / 2;
      floor.position.y = -6;
      floor.receiveShadow = true;
      scene.add(floor);

      // Texture loader
      textureLoader = new THREE.TextureLoader();

      // Canvas động cho chữ khắc Laser
      initEngraveCanvas();

      scene.add(strapGroup);

      // Tải mô hình dây da
      
      // Dựng dây da 3D bằng mã (Procedural Strap) thay vì dùng mô hình Handdn
      buildWatchAndStrap();

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
      animate();

      window.addEventListener('resize', onWindowResize);
    }

    // --- CANVAS TỰ ĐỘNG VẼ CHỮ KHẮC LASER 3D ---
    function initEngraveCanvas() {
      engraveTextureCanvas = document.createElement('canvas');
      engraveTextureCanvas.width = 512;
      engraveTextureCanvas.height = 128;
      engraveTextureContext = engraveTextureCanvas.getContext('2d');
      engraveTexture = new THREE.CanvasTexture(engraveTextureCanvas);
      updateEngraveTextureText('');
    }

    function updateEngraveTextureText(text) {
      const ctx = engraveTextureContext;
      ctx.fillStyle = '#C8B293'; // Màu da lót Zermatt
      ctx.fillRect(0, 0, 512, 128);

      if (text) {
        ctx.fillStyle = '#6E5539'; // Dập chìm màu sẫm
        ctx.font = 'bold 36px "Be Vietnam Pro", sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.letterSpacing = '4px';
        ctx.fillText(text.toUpperCase(), 256, 64);
      }
      engraveTexture.needsUpdate = true;
    }

    // --- DỰNG PROCEDURAL 3D MESH DÂY DA & KHÓA (KHÔNG CẦN BLENDER) ---
    function buildWatchAndStrap() {
      strapGroup = new THREE.Group();
      scene.add(strapGroup);

      // Tạo vật liệu da ban đầu
      const leatherMaterial = createLeatherMaterial(currentConfig.leather);

      // 1. DÂY NGẮN (Short Strap - Buckle Side)
      const shortCurve = new THREE.CubicBezierCurve3(
        new THREE.Vector3(0, 0, 3.8),     // Chân lug đồng hồ
        new THREE.Vector3(0, -0.8, 6.5),  // Bo cong theo cổ tay
        new THREE.Vector3(0, -2.5, 9.5),  // Thân giữa
        new THREE.Vector3(0, -4.5, 12.0)  // Chân khóa
      );
      shortStrapMesh = createCurvedStrapMesh(shortCurve, 2.0, 1.8, 0.32, leatherMaterial);
      shortStrapMesh.castShadow = true;
      strapGroup.add(shortStrapMesh);

      // 2. DÂY DÀI (Long Strap - Tail Side)
      const longCurve = new THREE.CubicBezierCurve3(
        new THREE.Vector3(0, 0, -3.8),     // Chân lug trên
        new THREE.Vector3(0, -0.8, -7.5),  // Bo cong ôm tay
        new THREE.Vector3(0, -3.2, -12.0), // Thân có lỗ
        new THREE.Vector3(0, -5.8, -16.5)  // Đuôi nhọn
      );
      longStrapMesh = createCurvedStrapMesh(longCurve, 2.0, 1.75, 0.32, leatherMaterial, true);
      longStrapMesh.castShadow = true;
      strapGroup.add(longStrapMesh);

      // 3. ĐỤC 7 LỖ KIM TRÊN DÂY DÀI
      createStrapHoles(strapGroup);

      // 4. ĐƯỜNG CHỈ MAY SADDLE STITCH VIỀN
      createStitching(shortCurve, longCurve);

      // 5. BỘ KHÓA KIM & ĐỈA DA
      buildBuckleAndKeepers(strapGroup, shortCurve.getPoint(1));

      // 6. MẶT ĐỒNG HỒ MẪU (Watch Case)
      buildWatchCase();

      // Cập nhật góc ban đầu
      strapGroup.rotation.y = Math.PI / 4;
    }

    // Hàm tạo thân dây uốn cong mượt mà theo đường cong Bezier
    function createCurvedStrapMesh(curve, widthStart, widthEnd, thickness, material, isPointed = false) {
      const segments = 36;
      const points = curve.getPoints(segments);
      const geom = new THREE.BufferGeometry();

      const vertices = [];
      const normals = [];
      const uvs = [];
      const indices = [];

      for (let i = 0; i <= segments; i++) {
        const t = i / segments;
        const p = points[i];
        const w = (widthStart + (widthEnd - widthStart) * t) / 2;
        
        // Đỉnh đuôi nhọn ở cuối nếu là dây dài
        const currentW = (isPointed && i === segments) ? 0.05 : w;

        // Vector tiếp tuyến & pháp tuyến
        const tangent = curve.getTangent(t).normalize();
        const normal = new THREE.Vector3(0, 1, 0);
        const side = new THREE.Vector3().crossVectors(tangent, normal).normalize();

        // 4 đỉnh mặt cắt (Top-Left, Top-Right, Bottom-Left, Bottom-Right)
        const tl = p.clone().addScaledVector(side, -currentW).addScaledVector(normal, thickness / 2);
        const tr = p.clone().addScaledVector(side, currentW).addScaledVector(normal, thickness / 2);
        const bl = p.clone().addScaledVector(side, -currentW).addScaledVector(normal, -thickness / 2);
        const br = p.clone().addScaledVector(side, currentW).addScaledVector(normal, -thickness / 2);

        vertices.push(tl.x, tl.y, tl.z,  tr.x, tr.y, tr.z,  bl.x, bl.y, bl.z,  br.x, br.y, br.z);
        normals.push(0, 1, 0,  0, 1, 0,  0, -1, 0,  0, -1, 0);
        uvs.push(0, t,  1, t,  0, t,  1, t);

        if (i < segments) {
          const base = i * 4;
          // Mặt trên
          indices.push(base, base + 1, base + 5,  base, base + 5, base + 4);
          // Mặt dưới
          indices.push(base + 2, base + 6, base + 7,  base + 2, base + 7, base + 3);
          // Viền trái (Sơn cạnh)
          indices.push(base, base + 4, base + 6,  base, base + 6, base + 2);
          // Viền phải (Sơn cạnh)
          indices.push(base + 1, base + 3, base + 7,  base + 1, base + 7, base + 5);
        }
      }

      geom.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
      geom.setAttribute('normal', new THREE.Float32BufferAttribute(normals, 3));
      geom.setAttribute('uv', new THREE.Float32BufferAttribute(uvs, 2));
      geom.setIndex(indices);
      geom.computeVertexNormals();

      return new THREE.Mesh(geom, material);
    }

    // Đục 7 lỗ xỏ kim tinh xảo
    function createStrapHoles(group) {
      const holeMaterial = new THREE.MeshBasicMaterial({ color: 0x1A1410 });
      for (let i = 0; i < 7; i++) {
        const holeGeo = new THREE.CylinderGeometry(0.08, 0.08, 0.38, 16);
        const hole = new THREE.Mesh(holeGeo, holeMaterial);
        // Định vị dọc theo đuôi dây dài
        hole.position.set(0, -2.5 - i * 0.42, -10.5 - i * 0.85);
        hole.rotation.x = 0.3;
        group.add(hole);
      }
    }

    // Dựng đường chỉ khâu tay nổi 3D
    function createStitching(shortCurve, longCurve) {
      const stitchMat = new THREE.MeshStandardMaterial({
        color: new THREE.Color(currentConfig.stitch.hex),
        roughness: 0.8,
        metalness: 0.05
      });

      function addStitchLine(curve, sideOffset, widthStart, widthEnd) {
        const count = 28;
        for (let i = 2; i < count; i++) {
          const t = i / count;
          const p = curve.getPoint(t);
          const tangent = curve.getTangent(t).normalize();
          const normal = new THREE.Vector3(0, 1, 0);
          const side = new THREE.Vector3().crossVectors(tangent, normal).normalize();
          const w = (widthStart + (widthEnd - widthStart) * t) / 2 - 0.14;

          const stitchGeo = new THREE.BoxGeometry(0.04, 0.035, 0.16);
          const stitch = new THREE.Mesh(stitchGeo, stitchMat);
          
          const pos = p.clone().addScaledVector(side, sideOffset * w).addScaledVector(normal, 0.17);
          stitch.position.copy(pos);
          stitch.quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, 1), tangent);
          stitch.rotation.y += (i % 2 === 0 ? 0.15 : -0.15); // Góc đan chỉ chéo thủ công
          strapGroup.add(stitch);
          stitchMeshes.push(stitch);
        }
      }

      addStitchLine(shortCurve, -1, 2.0, 1.8);
      addStitchLine(shortCurve, 1, 2.0, 1.8);
      addStitchLine(longCurve, -1, 2.0, 1.75);
      addStitchLine(longCurve, 1, 2.0, 1.75);
    }

    // Dựng Khóa kim & Đỉa da thật
    function buildBuckleAndKeepers(group, bucklePos) {
      buckleGroup = new THREE.Group();

      const metalMat = new THREE.MeshStandardMaterial({
        color: new THREE.Color(currentConfig.buckleMetal.hex),
        metalness: currentConfig.buckleMetal.metalness,
        roughness: currentConfig.buckleMetal.roughness
      });

      // 1. Khung khóa chữ U
      const frameGeo = new THREE.TorusGeometry(0.95, 0.09, 12, 24, Math.PI);
      const frame = new THREE.Mesh(frameGeo, metalMat);
      frame.rotation.x = Math.PI / 2;
      frame.position.set(0, 0, 0.3);
      buckleGroup.add(frame);

      // Chốt ngang
      const barGeo = new THREE.CylinderGeometry(0.06, 0.06, 1.9, 16);
      const bar = new THREE.Mesh(barGeo, metalMat);
      bar.rotation.z = Math.PI / 2;
      buckleGroup.add(bar);

      // Kim khóa
      const tongueGeo = new THREE.CylinderGeometry(0.04, 0.04, 1.1, 12);
      const tongue = new THREE.Mesh(tongueGeo, metalMat);
      tongue.position.set(0, 0.08, 0.45);
      tongue.rotation.x = -Math.PI / 2 - 0.2;
      buckleGroup.add(tongue);

      // 2. Hai con đỉa da (Fixed & Floating Keepers)
      const keeperMat = createLeatherMaterial(currentConfig.leather);
      const keeperGeo = new THREE.TorusGeometry(1.05, 0.12, 8, 20);

      const fixedKeeper = new THREE.Mesh(keeperGeo, keeperMat);
      fixedKeeper.scale.set(1, 0.45, 1);
      fixedKeeper.rotation.x = Math.PI / 2;
      fixedKeeper.position.set(0, 0, -0.8);
      buckleGroup.add(fixedKeeper);

      const floatKeeper = new THREE.Mesh(keeperGeo, keeperMat);
      floatKeeper.scale.set(1, 0.45, 1);
      floatKeeper.rotation.x = Math.PI / 2;
      floatKeeper.position.set(0, 0, -1.8);
      buckleGroup.add(floatKeeper);

      // Định vị toàn bộ cụm khóa vào đầu dây ngắn
      buckleGroup.position.copy(bucklePos);
      buckleGroup.position.y += 0.05;
      buckleGroup.rotation.x = 0.55;
      group.add(buckleGroup);
    }

    // Dựng Mặt Đồng Hồ Mẫu (Watch Case 40mm)
    function buildWatchCase() {
      watchGroup = new THREE.Group();

      const caseMetalMat = new THREE.MeshStandardMaterial({
        color: 0xE0E0E0,
        metalness: 0.95,
        roughness: 0.18
      });

      // Vỏ tròn
      const caseGeo = new THREE.CylinderGeometry(3.6, 3.6, 0.9, 48);
      const watchCase = new THREE.Mesh(caseGeo, caseMetalMat);
      watchCase.rotation.x = Math.PI / 2;
      watchCase.castShadow = true;
      watchGroup.add(watchCase);

      // Mặt Dial tròn đen sang trọng
      
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

      scene.add(watchGroup);
    }

    // Tạo Material PBR từ ảnh da thật của Percent kèm vân Normal Map
    function createLeatherMaterial(leatherItem) {
      if (!leatherTextures[leatherItem.id]) {
        const texPath = leatherItem.tex || leatherItem.img;
        const tex = textureLoader.load(texPath);
        tex.wrapS = THREE.RepeatWrapping;
        tex.wrapT = THREE.RepeatWrapping;
        tex.repeat.set(2.0, 6.0);
        leatherTextures[leatherItem.id] = tex;
      }

      if (leatherItem.norm && !leatherNormalMaps[leatherItem.id]) {
        const norm = textureLoader.load(leatherItem.norm);
        norm.wrapS = THREE.RepeatWrapping;
        norm.wrapT = THREE.RepeatWrapping;
        norm.repeat.set(2.0, 6.0);
        leatherNormalMaps[leatherItem.id] = norm;
      }

      const mat = new THREE.MeshStandardMaterial({
        color: new THREE.Color(leatherItem.hex),
        map: leatherTextures[leatherItem.id],
        normalMap: leatherNormalMaps[leatherItem.id] || null,
        normalScale: new THREE.Vector2(0.85, 0.85),
        roughness: leatherItem.roughness,
        metalness: 0.05
      });

      return mat;
    }


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
    function animate() {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    }

    function onWindowResize() {
      const container = document.querySelector('.viewport-container');
      camera.aspect = container.clientWidth / container.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(container.clientWidth, container.clientHeight);
    }

    // --- CÁC HÀM TƯƠNG TÁC CONFIGURATOR ---
    function selectLeather(leatherId) {
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
    }

    function selectStitch(stitchId) {
      const item = STITCH_COLORS.find(s => s.id === stitchId);
      if (!item) return;
      currentConfig.stitch = item;

      updateStitch();

      document.getElementById('val-stitch').innerText = item.name;
      document.querySelectorAll('.stitch-swatch').forEach(s => {
        s.classList.toggle('active', s.dataset.id === stitchId);
      });
    }

    function selectBuckleMetal(metalId) {
      const item = BUCKLE_METALS.find(m => m.id === metalId);
      if (!item) return;
      currentConfig.buckleMetal = item;

      update3D();

      document.getElementById('val-buckle').innerText = `${item.name} (${currentConfig.buckleType === 'tang' ? 'Khóa kim' : 'Khóa bướm'})`;
      document.querySelectorAll('.buckle-card').forEach(b => {
        b.classList.toggle('active', b.dataset.id === metalId);
      });
    }

    function setBuckleType(type, el) {
      currentConfig.buckleType = type;
      el.parentElement.querySelectorAll('.size-pill').forEach(p => p.classList.remove('active'));
      el.classList.add('active');
      selectBuckleMetal(currentConfig.buckleMetal.id);
      updatePrice();
    }

    function setLugSize(size, el) {
      currentConfig.lugSize = size;
      el.parentElement.querySelectorAll('.size-pill').forEach(p => p.classList.remove('active'));
      el.classList.add('active');
      document.getElementById('val-lug').innerText = size;
    }

    function setWristSize(size, el) {
      currentConfig.wristSize = size;
      el.parentElement.querySelectorAll('.size-pill').forEach(p => p.classList.remove('active'));
      el.classList.add('active');
      document.getElementById('val-wrist').innerText = size;
    }

    function updateEngraving(text) {
      currentConfig.engraving = text;
      updateEngraveTextureText(text);
    }

    function updatePrice() {
      let total = currentConfig.leather.price;
      if (currentConfig.buckleType === 'deployant') {
        total += 150000;
      }
      document.getElementById('total-price').innerText = new Intl.NumberFormat('vi-VN').format(total) + '₫';
    }

    // --- CÁC GÓC NHÌN CAMERA PRESET ---
    function setCameraView(preset) {
      document.querySelectorAll('.camera-presets .vp-btn').forEach(b => b.classList.remove('active'));
      if(event) event.target.classList.add('active');

      switch(preset) {
        case 'overview':
          animateCamera(0, 18, 28, 0, 0, 0);
          break;
        case 'buckle':
          animateCamera(0, 5, 20, 0, -4, 12);
          break;
        case 'tail':
          animateCamera(0, 2, -22, 0, -5, -14);
          break;
        case 'lining':
          animateCamera(0, -18, 15, 0, 0, 0);
          break;
      }
    }

    function animateCamera(x, y, z, tx, ty, tz) {
      const startPos = camera.position.clone();
      const endPos = new THREE.Vector3(x, y, z);
      const startTarget = controls.target.clone();
      const endTarget = new THREE.Vector3(tx, ty, tz);

      let progress = 0;
      function step() {
        progress += 0.04;
        if (progress <= 1) {
          camera.position.lerpVectors(startPos, endPos, progress);
          controls.target.lerpVectors(startTarget, endTarget, progress);
          requestAnimationFrame(step);
        } else {
          camera.position.copy(endPos);
          controls.target.copy(endTarget);
        }
      }
      step();
    }

    function toggleWatchCase() {
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
    
    function setWatchFace(faceId, el) {
        const face = WATCH_FACES.find(f => f.id === faceId);
        if(!face) return;
        currentConfig.watchFace = face;
        
        document.getElementById('val-watchface').innerText = face.name;
        document.querySelectorAll('.watchface-pill').forEach(p => p.classList.remove('active'));
        if(el) el.classList.add('active');
        else if(typeof event !== 'undefined' && event && event.target) event.target.classList.add('active');
        
        if(currentConfig.showWatch) {
            loadWatchFace(face);
        }
    }
    

    function toggleAutoRotate() {
      currentConfig.autoRotate = !currentConfig.autoRotate;
      const btn = document.getElementById('btn-toggle-rotate');
      if (btn) btn.classList.toggle('active', currentConfig.autoRotate);
      controls.autoRotate = currentConfig.autoRotate;
    }

    // Chụp snapshot tải về
    function captureSnapshot() {
      renderer.render(scene, camera);
      const dataURL = renderer.domElement.toDataURL('image/png');
      const a = document.createElement('a');
      a.href = dataURL;
      a.download = `percent-3d-${currentConfig.leather.id}.png`;
      a.click();
      confetti({ particleCount: 50, spread: 60, origin: { y: 0.8 } });
    }

    // Modal Checkout
    function openCheckoutModal() {
      let total = currentConfig.leather.price + (currentConfig.buckleType === 'deployant' ? 150000 : 0);
      const html = `
        <div class="summary-row"><span class="summary-label">Mẫu Dây Da:</span><span class="summary-val">${currentConfig.leather.name} (${currentConfig.leather.color})</span></div>
        <div class="summary-row"><span class="summary-label">Màu Chỉ May:</span><span class="summary-val">${currentConfig.stitch.name}</span></div>
        <div class="summary-row"><span class="summary-label">Kiểu Khóa:</span><span class="summary-val">${currentConfig.buckleType === 'tang' ? 'Khóa Kim' : 'Khóa Bướm'} (${currentConfig.buckleMetal.name})</span></div>
        <div class="summary-row"><span class="summary-label">Size Dây:</span><span class="summary-val">${currentConfig.lugSize}</span></div>
        <div class="summary-row"><span class="summary-label">Chu Vi Tay:</span><span class="summary-val">${currentConfig.wristSize}</span></div>
        <div class="summary-row"><span class="summary-label">Khắc Laser:</span><span class="summary-val">${currentConfig.engraving || 'Không khắc'}</span></div>
        <div class="summary-row" style="margin-top: 10px; padding-top: 8px; border-top: 1px dashed var(--pc-border); font-size: 14px;"><span class="summary-label" style="font-weight: 700; color: var(--pc-espresso);">Tổng Thanh Toán:</span><span class="summary-val" style="color: var(--pc-cognac); font-size: 16px;">${new Intl.NumberFormat('vi-VN').format(total)}₫</span></div>
      `;
      document.getElementById('summary-content').innerHTML = html;
      document.getElementById('checkout-modal').style.display = 'flex';
      confetti({ particleCount: 80, spread: 70, origin: { y: 0.6 } });
    }

    function closeCheckoutModal() {
      document.getElementById('checkout-modal').style.display = 'none';
    }

    function sendOrderZalo() {
      const msg = `Xin chào Percent! Tôi muốn đặt may bộ dây da 3D:
- Dòng: ${currentConfig.leather.name} (${currentConfig.leather.color})
- Chỉ: ${currentConfig.stitch.name}
- Khóa: ${currentConfig.buckleType === 'tang' ? 'Khóa Kim' : 'Khóa Bướm'} (${currentConfig.buckleMetal.name})
- Size lug: ${currentConfig.lugSize} | Cổ tay: ${currentConfig.wristSize}
- Khắc tên: ${currentConfig.engraving || 'Không'}
Nhờ xưởng tư vấn và chế tác giúp tôi!`;
      window.open(`https://zalo.me/0902678910?text=${encodeURIComponent(msg)}`, '_blank');
    }

    function sendOrderShopDongHo() {
      alert('Đã đóng gói dữ liệu cấu hình 3D! Trong bản live trên web, thông số này sẽ tự động chuyển thẳng vào giỏ hàng WooCommerce của shopdongho.com.');
    }

    // --- RENDER GIAO DIỆN KHỞI TẠO ---
    function renderUI() {
      // 1. Grid da
      const lGrid = document.getElementById('leather-grid');
      lGrid.innerHTML = LEATHER_CATALOG.map((l, idx) => `
        <div class="leather-card ${idx === 0 ? 'active' : ''}" data-id="${l.id}" onclick="selectLeather('${l.id}')">
          <div class="leather-img-wrap">
            <img src="${l.img}" alt="${l.name}">
          </div>
          <div class="leather-name">${l.name.replace('Percent ', '')}</div>
          <div class="leather-color-tag">${l.color}</div>
          <div class="leather-price">${new Intl.NumberFormat('vi-VN').format(l.price)}₫</div>
        </div>
      `).join('');

      // 2. Swatch chỉ may
      const sGroup = document.getElementById('stitch-group');
      sGroup.innerHTML = STITCH_COLORS.map((s, idx) => `
        <div class="stitch-swatch ${idx === 0 ? 'active' : ''}" data-id="${s.id}" onclick="selectStitch('${s.id}')">
          <div class="stitch-dot" style="background: ${s.hex};"></div>
          <span class="stitch-label">${s.name.split(' ')[1] || s.name}</span>
        </div>
      `).join('');

      // 3. Grid khóa
      const bGrid = document.getElementById('buckle-grid');
      bGrid.innerHTML = BUCKLE_METALS.map((b, idx) => `
        <div class="buckle-card ${idx === 0 ? 'active' : ''}" data-id="${b.id}" onclick="selectBuckleMetal('${b.id}')">
          <div class="buckle-metal-pill" style="background: ${b.hex};"></div>
          <div class="buckle-name">${b.name}</div>
        </div>
      `).join('');
    }

    // Khởi động khi tải xong trang
    window.addEventListener('DOMContentLoaded', () => {
      renderUI();
      init3D();
      updatePrice();
    });
  </script>
