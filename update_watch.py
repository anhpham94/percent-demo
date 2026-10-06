import re

with open('3d.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add Canvas texture for watch dial
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
                    // Vẽ số La Mã
                    const numerals = ['XII', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI'];
                    ctx.font = 'bold 40px serif';
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.fillText(numerals[i], 0, -190);
                } else if (style === 'Minimal') {
                    // Vạch mảnh
                    ctx.fillRect(-2, -220, 4, 30);
                } else {
                    // Vạch đậm
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

content = content.replace("// Khởi tạo SCENE", canvas_code + "\n        // Khởi tạo SCENE")

# Change watch dial material to use texture
dial_mat = """
            watchDialMaterial = new THREE.MeshPhysicalMaterial({ 
                color: 0xffffff,
                metalness: 0.1,
                roughness: 0.8,
                map: dialTextures.white_classic
            });
"""
content = re.sub(r'watchDialMaterial = new THREE\.MeshPhysicalMaterial\(\{[\s\S]*?\}\);', dial_mat, content)

# Modify UI for Watch Faces
ui_code = """
            <div class="option-group">
                <div class="option-title">Mặt Số (Watch Face)</div>
                <div class="option-list" id="dial-options">
                    <button class="option-btn active" data-val="white_classic" data-type="dial">Classic White</button>
                    <button class="option-btn" data-val="black_minimal" data-type="dial">Minimal Black</button>
                    <button class="option-btn" data-val="blue_roman" data-type="dial">Blue Roman</button>
                </div>
            </div>
"""
content = re.sub(r'<div class="option-group">[\s\S]*?<div class="option-title">Mặt số</div>[\s\S]*?</div>', ui_code, content)

# Add event listener for Dial
js_code = """
            document.querySelectorAll('#dial-options .option-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    document.querySelectorAll('#dial-options .option-btn').forEach(b => b.classList.remove('active'));
                    e.target.classList.add('active');
                    const val = e.target.dataset.val;
                    if(watchDialMaterial) {
                        watchDialMaterial.map = dialTextures[val];
                        watchDialMaterial.needsUpdate = true;
                    }
                });
            });
"""
content = content.replace("initUI();", "initUI();\n" + js_code)

with open('3d.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated watch face logic")
