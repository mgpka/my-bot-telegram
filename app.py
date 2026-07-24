<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>الأمراء | 𝔞𝔩 𝔭𝔯𝔧𝔫𝔠𝔢𝔰</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            user-select: none;
        }

        body {
            background-color: #000000;
            color: #ffffff;
            height: 100vh;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            padding: 20px;
        }

        /* العنوان العلوي */
        .header-title {
            font-size: 26px;
            font-weight: bold;
            color: #ffffff;
            text-align: center;
            margin-top: 15px;
            letter-spacing: 2px;
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
            z-index: 10;
        }

        /* حاوية العرض الـ 3D */
        #canvas-container {
            width: 100%;
            height: 55vh;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: grab;
            z-index: 5;
        }
        #canvas-container:active {
            cursor: grabbing;
        }

        /* شريط الأزرار السفلي */
        .button-bar {
            display: flex;
            gap: 20px;
            margin-bottom: 25px;
            z-index: 10;
            width: 100%;
            max-width: 380px;
        }

        .btn {
            flex: 1;
            padding: 14px 20px;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            color: white;
            text-align: center;
        }

        .btn-green {
            background-color: #28a745;
            box-shadow: 0 4px 15px rgba(40, 167, 69, 0.4);
        }
        .btn-green:hover {
            background-color: #218838;
            transform: translateY(-2px);
        }

        .btn-red {
            background-color: #dc3545;
            box-shadow: 0 4px 15px rgba(220, 53, 69, 0.4);
        }
        .btn-red:hover {
            background-color: #c82333;
            transform: translateY(-2px);
        }

        /* النوافذ المنبثقة (Modal) */
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.85);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 100;
            backdrop-filter: blur(5px);
        }

        .modal-card {
            background: #111111;
            border: 1px solid #333;
            border-radius: 12px;
            padding: 25px;
            width: 90%;
            max-width: 400px;
            box-shadow: 0 0 25px rgba(255, 255, 255, 0.1);
            text-align: center;
        }

        .modal-card h3 {
            margin-bottom: 20px;
            font-size: 20px;
            color: #fff;
            line-height: 1.5;
        }

        .form-group {
            margin-bottom: 15px;
            text-align: right;
        }

        .form-group label {
            display: block;
            margin-bottom: 6px;
            font-size: 14px;
            color: #bbb;
        }

        .form-group input {
            width: 100%;
            padding: 12px;
            border-radius: 6px;
            border: 1px solid #444;
            background: #222;
            color: #fff;
            font-size: 15px;
            outline: none;
            direction: ltr;
            text-align: right;
        }

        .form-group input:focus {
            border-color: #28a745;
        }

        .error-msg {
            color: #ff4d4d;
            font-size: 13px;
            margin-top: 10px;
            display: none;
            text-align: center;
            background: rgba(255, 77, 77, 0.1);
            padding: 8px;
            border-radius: 4px;
        }

        .modal-btns {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }

        /* زر لوحة التحكم المخفي/السفلي */
        .admin-link {
            position: fixed;
            bottom: 5px;
            left: 10px;
            font-size: 11px;
            color: #333;
            cursor: pointer;
            z-index: 10;
        }
        .admin-link:hover { color: #666; }

        /* جدول الأدمن */
        .admin-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            font-size: 13px;
        }
        .admin-table th, .admin-table td {
            border: 1px solid #333;
            padding: 8px;
            text-align: center;
        }
        .admin-table th { background: #222; }
        .btn-delete {
            background: #dc3545;
            color: white;
            border: none;
            padding: 4px 8px;
            border-radius: 4px;
            cursor: pointer;
        }
    </style>
</head>
<body>

    <div class="header-title">
        الأمراء | 𝔞𝔩 𝔭𝔯𝔧𝔫𝔠𝔢𝔰
    </div>

    <div id="canvas-container"></div>

    <div class="button-bar">
        <button class="btn btn-green" onclick="openConfirmModal()">المشاركة</button>
        <button class="btn btn-red" onclick="exitSite()">عدم المشاركة</button>
    </div>

    <div class="admin-link" onclick="openAdminLogin()">لوحة التحكم ⚙️</div>

    <div class="modal-overlay" id="confirmModal">
        <div class="modal-card">
            <h3>هل أنت تأكد من أنك تريد المشاركة في هذه اللعبة؟</h3>
            <div class="modal-btns">
                <button class="btn btn-green" onclick="goToForm()">نعم</button>
                <button class="btn btn-red" onclick="closeConfirmModal()">لا</button>
            </div>
        </div>
    </div>

    <div class="modal-overlay" id="formModal">
        <div class="modal-card">
            <h3>للمشاركة املأ الحقول التالية</h3>
            
            <div class="form-group">
                <label>الحقل الأول: الاسم</label>
                <input type="text" id="playerName" placeholder="أدخل اسمك الكامل">
            </div>

            <div class="form-group">
                <label>الحقل الثاني: اختر رقم من 1 إلى 30</label>
                <input type="number" id="playerNumber" placeholder="مثال: 15" min="1" max="30">
            </div>

            <div class="form-group">
                <label>الحقل الثالث: يوزر التليجرام</label>
                <input type="text" id="playerTelegram" placeholder="مثال: @username">
            </div>

            <div class="error-msg" id="formError"></div>

            <div class="modal-btns">
                <button class="btn btn-green" onclick="submitRegistration()">تأكيد التسجيل</button>
                <button class="btn btn-red" style="background:#555;" onclick="closeFormModal()">إلغاء</button>
            </div>
        </div>
    </div>

    <div class="modal-overlay" id="adminLoginModal">
        <div class="modal-card">
            <h3>تسجيل دخول لوحة التحكم</h3>
            <div class="form-group">
                <label>الإيميل</label>
                <input type="email" id="adminEmail" placeholder="الإيميل">
            </div>
            <div class="form-group">
                <label>كلمة السر</label>
                <input type="password" id="adminPass" placeholder="كلمة السر">
            </div>
            <div class="error-msg" id="adminError"></div>
            <div class="modal-btns">
                <button class="btn btn-green" onclick="loginAdmin()">دخول</button>
                <button class="btn btn-red" style="background:#555;" onclick="closeAdminLogin()">إغلاق</button>
            </div>
        </div>
    </div>

    <div class="modal-overlay" id="adminDashboardModal">
        <div class="modal-card" style="max-width: 550px; max-height: 80vh; overflow-y: auto;">
            <h3>قائمة المشاركين المسجلين</h3>
            <table class="admin-table">
                <thead>
                    <tr>
                        <th>الاسم</th>
                        <th>الرقم</th>
                        <th>التليجرام</th>
                        <th>حذف</th>
                    </tr>
                </thead>
                <tbody id="adminTableBody">
                    </tbody>
            </table>
            <div style="margin-top: 15px;">
                <button class="btn btn-red" style="padding: 8px 15px; font-size: 14px;" onclick="closeAdminDashboard()">إغلاق اللوحة</button>
            </div>
        </div>
    </div>

    <iframe id="ytPlayer" style="display:none;" 
            src="https://www.youtube.com/embed/q7uTnxYFDSw?enablejsapi=1&autoplay=1&loop=1&playlist=q7uTnxYFDSw" 
            allow="autoplay">
    </iframe>

    <script>
        // --- 1. إعداد الموسيقى التلقائية عند التفاعل ---
        let audioStarted = false;
        function startAudio() {
            if (!audioStarted) {
                const iframe = document.getElementById('ytPlayer');
                iframe.contentWindow.postMessage('{"event":"command","func":"playVideo","args":""}', '*');
                audioStarted = true;
            }
        }
        window.addEventListener('click', startAudio);
        window.addEventListener('touchstart', startAudio);

        // --- 2. إعداد العرض الـ 3D باستخدام Three.js ---
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });

        renderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(renderer.domElement);

        // إضاءة المشهد
        const ambientLight = new THREE.AmbientLight(0xffffff, 1.2);
        scene.add(ambientLight);

        // إنشاء كرت / صورة 3D
        const geometry = new THREE.BoxGeometry(2.8, 3.8, 0.08);
        
        // تجهيز نسيج الصورة (يمكنك وضع رابط صورتك هنا بدلاً من الصورة الافتراضية)
        const textureLoader = new THREE.TextureLoader();
        const cardTexture = textureLoader.load('https://picsum.photos/400/600'); // صورة توضيحية افتراضية عالية الجودة

        const materials = [
            new THREE.MeshBasicMaterial({ color: 0x111111 }), // يمين
            new THREE.MeshBasicMaterial({ color: 0x111111 }), // يسار
            new THREE.MeshBasicMaterial({ color: 0x111111 }), // أعلى
            new THREE.MeshBasicMaterial({ color: 0x111111 }), // أسفل
            new THREE.MeshBasicMaterial({ map: cardTexture }), // الوجه الأمامي
            new THREE.MeshBasicMaterial({ color: 0x1a1a1a })  // الوجه الخلفي
        ];

        const card = new THREE.Mesh(geometry, materials);
        scene.add(card);
        camera.position.z = 6;

        // التحريك التفاعلي بالماوس / اللمس (3D Drag & Flip)
        let isDragging = false;
        let previousMousePosition = { x: 0, y: 0 };

        function onPointerDown(e) {
            isDragging = true;
            previousMousePosition = {
                x: e.clientX || (e.touches && e.touches[0].clientX),
                y: e.clientY || (e.touches && e.touches[0].clientY)
            };
        }

        function onPointerMove(e) {
            if (!isDragging) return;
            const currentX = e.clientX || (e.touches && e.touches[0].clientX);
            const currentY = e.clientY || (e.touches && e.touches[0].clientY);

            const deltaX = currentX - previousMousePosition.x;
            const deltaY = currentY - previousMousePosition.y;

            card.rotation.y += deltaX * 0.01;
            card.rotation.x += deltaY * 0.01;

            previousMousePosition = { x: currentX, y: currentY };
        }

        function onPointerUp() { isDragging = false; }

        container.addEventListener('mousedown', onPointerDown);
        window.addEventListener('mousemove', onPointerMove);
        window.addEventListener('mouseup', onPointerUp);

        container.addEventListener('touchstart', onPointerDown);
        window.addEventListener('touchmove', onPointerMove);
        window.addEventListener('touchend', onPointerUp);

        // حلقة العرض والدوران البسيط عند التوقف
        function animate() {
            requestAnimationFrame(animate);
            if (!isDragging) {
                card.rotation.y += 0.003;
            }
            renderer.render(scene, camera);
        }
        animate();

        // إعادة ضبط الحجم عند تغيير حجم الشاشة
        window.addEventListener('resize', () => {
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
        });


        // --- 3. قواعد البيانات والمنطق البرمجي (Local & Global State) ---
        function getParticipants() {
            return JSON.parse(localStorage.getItem('princes_participants') || '[]');
        }

        function saveParticipants(data) {
            localStorage.setItem('princes_participants', JSON.stringify(data));
        }

        // --- 4. وظائف النوافذ والأزرار ---
        function openConfirmModal() {
            document.getElementById('confirmModal').style.display = 'flex';
        }

        function closeConfirmModal() {
            document.getElementById('confirmModal').style.display = 'none';
        }

        function goToForm() {
            closeConfirmModal();
            document.getElementById('formModal').style.display = 'flex';
        }

        function closeFormModal() {
            document.getElementById('formModal').style.display = 'none';
            document.getElementById('formError').style.display = 'none';
        }

        // الزر الأحمر (خروج)
        function exitSite() {
            window.location.href = "about:blank";
            window.close();
        }

        // تسجيل المشارك والتحقق من الشروط
        function submitRegistration() {
            const name = document.getElementById('playerName').value.trim();
            const number = parseInt(document.getElementById('playerNumber').value);
            const telegram = document.getElementById('playerTelegram').value.trim();
            const errorDiv = document.getElementById('formError');

            errorDiv.style.display = 'none';
            errorDiv.innerText = '';

            // فحص الاسم
            if (!name) {
                showError('يرجى كتابة الاسم بشكل صحيح');
                return;
            }

            // فحص الرقم (من 1 إلى 30)
            if (isNaN(number) || number < 1 || number > 30) {
                showError('خطأ: اختر رقم بين 1 و 30 فقط');
                return;
            }

            // فحص توفر الرقم
            const participants = getParticipants();
            const numberTaken = participants.some(p => p.number === number);
            if (numberTaken) {
                showError('الرقم محجوز اختر رقم اخر');
                return;
            }

            // فحص التليجرام والرمز @
            if (!telegram.startsWith('@')) {
                showError('اكتب يوزرك ب الشكل الاتي مثال @mgpka باستخدام @');
                return;
            }

            // حظر اليوزر المحدد
            if (telegram.toLowerCase() === '@mgpka') {
                showError('هذا اليوزر غير مسموح باستخدامه');
                return;
            }

            // حفظ المشارك
            participants.push({ name, number, telegram });
            saveParticipants(participants);

            alert('تم تسجيل مشاركتك بنجاح في اللعبة! 🎯');
            closeFormModal();
            // تفريغ الحقول
            document.getElementById('playerName').value = '';
            document.getElementById('playerNumber').value = '';
            document.getElementById('playerTelegram').value = '';
        }

        function showError(msg) {
            const errorDiv = document.getElementById('formError');
            errorDiv.innerText = msg;
            errorDiv.style.display = 'block';
        }

        // --- 5. لوحة التحكم (Admin Panel) ---
        function openAdminLogin() {
            document.getElementById('adminLoginModal').style.display = 'flex';
        }

        function closeAdminLogin() {
            document.getElementById('adminLoginModal').style.display = 'none';
            document.getElementById('adminError').style.display = 'none';
        }

        function loginAdmin() {
            const email = document.getElementById('adminEmail').value.trim();
            const pass = document.getElementById('adminPass').value.trim();
            const err = document.getElementById('adminError');

            if (email === 'alinael2018fa@gmail.com' && pass === 'alinael2018qwer') {
                closeAdminLogin();
                openAdminDashboard();
            } else {
                err.innerText = 'الإيميل أو كلمة السر غير صحيحة!';
                err.style.display = 'block';
            }
        }

        function openAdminDashboard() {
            document.getElementById('adminDashboardModal').style.display = 'flex';
            renderAdminTable();
        }

        function closeAdminDashboard() {
            document.getElementById('adminDashboardModal').style.display = 'none';
        }

        function renderAdminTable() {
            const tbody = document.getElementById('adminTableBody');
            tbody.innerHTML = '';
            const participants = getParticipants();

            if (participants.length === 0) {
                tbody.innerHTML = '<tr><td colspan="4">لا يوجد مشاركين مسجلين حالياً</td></tr>';
                return;
            }

            participants.forEach((p, index) => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${p.name}</td>
                    <td><b>${p.number}</b></td>
                    <td>${p.telegram}</td>
                    <td><button class="btn-delete" onclick="deleteParticipant(${index})">حذف</button></td>
                `;
                tbody.appendChild(tr);
            });
        }

        function deleteParticipant(index) {
            if (confirm('هل أنت تأكد من حذف هذا المشارك؟ سيتم إتاحة رقمه للجميع مجدداً.')) {
                let participants = getParticipants();
                participants.splice(index, 1);
                saveParticipants(participants);
                renderAdminTable();
            }
        }
    </script>
</body>
</html>
