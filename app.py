import os
import json
import threading
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from waitress import serve

# ==================== الإعدادات الأساسية ====================
BOT_TOKEN = "8675694596:AAF8F8-CqsykzYnFhBZs8s1hRNHdbANftZA"
ADMIN_ID = 1460392381
MAX_PARTICIPANTS = 100
DATA_FILE = "participants.json"
PORT = 5000  # منفذ السيرفر المحلي

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)
WEB_URL = "https://e5c80a3c094e3e.lhr.life"
# ==================== إدارة البيانات ====================
def load_participants():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_participant(user_info):
    participants = load_participants()
    
    # فحص التكرار
    for p in participants:
        if str(p.get("id")) == str(user_info.get("id")):
            return False, "أنت مسجل بالفعل في اللعبة!"
            
    # فحص الحد الأقصى (100 لاعب)
    if len(participants) >= MAX_PARTICIPANTS:
        return False, "عذراً، اكتمل العدد الأقصى للمشاركين (100 لاعب)!"
        
    user_info["date"] = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    participants.append(user_info)
    
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(participants, f, ensure_ascii=False, indent=2)
        
    return True, "تم تسجيلك بنجاح!"

# ==================== تصميم الموقع (HTML/CSS/JS) ====================
HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>الأمراء | Squid Game</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
        body {
            background-color: #080808;
            color: #fff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            min-height: 100vh;
            padding: 20px 10px;
            overflow-x: hidden;
        }
        .header-title {
            font-size: 22px;
            font-weight: bold;
            color: #d4af37;
            text-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
            margin-top: 10px;
            letter-spacing: 1px;
            text-align: center;
        }
        /* كارت 3D تفاعلي */
        .card-container {
            perspective: 1000px;
            width: 320px;
            height: 200px;
            margin: 20px 0;
            cursor: pointer;
        }
        .card-3d {
            width: 100%;
            height: 100%;
            position: relative;
            transform-style: preserve-3d;
            transition: transform 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(229, 9, 20, 0.3);
        }
        .card-3d.flipped {
            transform: rotateY(180deg);
        }
        .card-face {
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            border-radius: 12px;
            border: 2px solid #d4af37;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            background: #111;
        }
        .card-face img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .card-back {
            transform: rotateY(180deg);
        }
        
        .buttons-container {
            width: 100%;
            max-width: 320px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-bottom: 20px;
        }
        .btn {
            padding: 14px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
            text-align: center;
        }
        .btn-join {
            background-color: #27ae60;
            color: #fff;
            box-shadow: 0 4px 15px rgba(39, 174, 96, 0.4);
        }
        .btn-join:active { transform: scale(0.98); }
        .btn-leave {
            background-color: #c0392b;
            color: #fff;
            box-shadow: 0 4px 15px rgba(192, 57, 43, 0.4);
        }
        
        /* نافذة التأكيد Pop-up */
        .modal-overlay {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0, 0, 0, 0.85);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 100;
        }
        .modal-box {
            background: #181818;
            border: 1px solid #d4af37;
            padding: 20px;
            border-radius: 12px;
            width: 85%;
            max-width: 300px;
            text-align: center;
        }
        .modal-box p { margin-bottom: 20px; font-size: 15px; line-height: 1.5; }
        .modal-btns { display: flex; gap: 10px; justify-content: center; }
        .modal-btns button {
            flex: 1; padding: 10px; border: none; border-radius: 6px; font-weight: bold; cursor: pointer;
        }
        .btn-yes { background: #27ae60; color: #fff; }
        .btn-no { background: #555; color: #fff; }
    </style>
</head>
<body>

    <div class="header-title">الأمراء | 𝔞𝔩 𝔭𝔯𝔧𝔫𝔠𝔢𝔰</div>

    <!-- بطاقة 3D -->
    <div class="card-container" onclick="flipCard()">
        <div class="card-3d" id="card">
            <div class="card-face card-front">
                <img src="/static/image1.jpg" alt="Squid Game Welcome" onerror="this.src='https://via.placeholder.com/320x200/111/d4af37?text=Welcome+Squid+Game'">
            </div>
            <div class="card-face card-back">
                <img src="/static/image2.jpg" alt="Squid Game Symbols" onerror="this.src='https://via.placeholder.com/320x200/111/d4af37?text=Symbols+Circle+Triangle+Square'">
            </div>
        </div>
    </div>

    <!-- الأزرار السفليّة -->
    <div class="buttons-container">
        <button class="btn btn-join" onclick="showModal()">المشاركة</button>
        <button class="btn btn-leave" onclick="exitApp()">عدم المشاركة</button>
    </div>

    <!-- نافذة التأكيد -->
    <div class="modal-overlay" id="modal">
        <div class="modal-box">
            <p>هل أنت متأكد من أنك تريد المشاركة في هذه اللعبة؟</p>
            <div class="modal-btns">
                <button class="btn-yes" onclick="confirmJoin()">نعم</button>
                <button class="btn-no" onclick="hideModal()">لا</button>
            </div>
        </div>
    </div>

    <!-- صوتية Pink Soldiers (تكرارية مستمرة) -->
    <audio id="bgAudio" loop preload="auto">
        <source src="https://ia801503.us.archive.org/15/items/pink-soldiers-squid-game-ost/Pink%20Soldiers.mp3" type="audio/mpeg">
    </audio>

    <script>
        const tg = window.Telegram?.WebApp;
        if(tg) { tg.ready(); tg.expand(); }

        const audio = document.getElementById("bgAudio");

        // تشغيل الصوت عند أول لمسة للشاشة (لتجاوز سياسة المتصفح)
        function startAudio() {
            audio.play().catch(() => {});
            document.removeEventListener('touchstart', startAudio);
            document.removeEventListener('click', startAudio);
        }
        document.addEventListener('touchstart', startAudio);
        document.addEventListener('click', startAudio);

        function flipCard() {
            document.getElementById("card").classList.toggle("flipped");
        }

        function showModal() { document.getElementById("modal").style.display = "flex"; }
        function hideModal() { document.getElementById("modal").style.display = "none"; }

        function exitApp() {
            audio.pause();
            if(tg) tg.close();
            else alert("تم الخروج من الصفحة.");
        }

        function confirmJoin() {
            const user = tg?.initDataUnsafe?.user || { id: "1460392381", first_name: "تجربة", username: "TestUser" };
            
            fetch('/api/join', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(user)
            })
            .then(res => res.json())
            .then(data => {
                alert(data.message);
                if(data.success) {
                    audio.pause();
                    if(tg) tg.close();
                } else {
                    hideModal();
                }
            })
            .catch(() => {
                alert("حدث خطأ في الاتصال بالسيرفر!");
                hideModal();
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/api/join', methods=['POST'])
def api_join():
    data = request.json or {}
    user_info = {
        "id": data.get("id", "غير معروف"),
        "name": data.get("first_name", "غير معروف"),
        "username": data.get("username", "لا يوجد")
    }
    
    success, msg = save_participant(user_info)
    
    if success:
        # إرسال إشعار فوري للأدمن حصراً
        text = (
            f"🎯 **تم مشاركة لاعب جديد!**\n\n"
            f"👤 **الاسم:** {user_info['name']}\n"
            f"🔗 **اليوزر:** @{user_info['username']}\n"
            f"🆔 **الايدي:** `{user_info['id']}`\n"
            f"📅 **الوقت:** {user_info['date']}"
        )
        try:
            bot.send_message(ADMIN_ID, text, parse_mode="Markdown")
        except Exception as e:
            print(f"Error sending notification: {e}")
            
    return jsonify({"success": success, "message": msg})

# ==================== بوت تليجرام ====================
@bot.message_handler(commands=['start'])
def handle_start(message):
    # التأكد من أن المستخدم هو الأدمن فقط
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "عذراً، هذا البوت خاص بالإدارة فقط.")
        return

    markup = InlineKeyboardMarkup()
    btn_count = InlineKeyboardButton("📊 عدد المشاركين التفاصيل", callback_data="show_details")
    
    # تحذير: يتطلب رابط HTTPS لتشغيله كـ WebApp داخل تليجرام
    web_url = "https://e5c80a3c094e3e.lhr.life"
    btn_site = InlineKeyboardButton("🎮 موقع المشاركة", web_app=WebAppInfo(url=web_url))
    
    markup.add(btn_count)
    markup.add(btn_site)
    
    bot.send_message(
        ADMIN_ID,
        "أهلاً بك يا أدمن! التحكم الكامل باللعبة والمشاركين بين يديك الآن:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "show_details")
def callback_details(call):
    if call.from_user.id != ADMIN_ID:
        return
        
    participants = load_participants()
    count = len(participants)
    
    msg = f"📊 **إجمالي المشاركين:** `{count} / {MAX_PARTICIPANTS}`\n\n"
    if count == 0:
        msg += "لا يوجد مشاركين حتى الآن."
    else:
        for i, p in enumerate(participants, 1):
            msg += f"{i}. {p['name']} | @{p['username']} | `{p['id']}`\n   📅 {p['date']}\n"
            
    bot.send_message(ADMIN_ID, msg, parse_mode="Markdown")

# ==================== التشغيل المتزامن ====================
def run_flask():
    print(f"🚀 السيرفر يعمل الآن على المنفذ {PORT} بكفاءة عالية (تزامن 40+ لاعب)...")
    serve(app, host="0.0.0.0", port=PORT, threads=50)

if __name__ == "__main__":
    # تشغيل السيرفر في خيط مستقل
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()
    
    # تشغيل البوت
    print("🤖 البوت شغال وجاهز لاستقبال الأوامر...")
    bot.infinity_polling()