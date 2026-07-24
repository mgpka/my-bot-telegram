from datetime import datetime
import json
import os
from flask import Flask, jsonify, redirect, render_template_string, request, url_for

app = Flask(__name__, static_folder='static', static_url_path='/static')
DATA_FILE = 'participants.json'


# تحميل البيانات
def load_participants():
  if not os.path.exists(DATA_FILE):
    return []
  try:
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
      return json.load(f)
  except:
    return []


# حفظ البيانات
def save_participant(name, username):
  participants = load_participants()
  # إضافة المشارك جديد
  new_entry = {
      'id': len(participants) + 1,
      'name': name,
      'username': (
          username if username.startswith('@') else f'@{username}'
      ),
      'date': datetime.now().strftime('%Y-%m-%d %I:%M:%S %p'),
  }
  participants.append(new_entry)
  with open(DATA_FILE, 'w', encoding='utf-8') as f:
    json.dump(participants, f, ensure_ascii=False, indent=4)


# 1️⃣ الصفحة الرئيسية للمستخدمين
@app.route('/')
def index():
  return render_template_string("""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>المشاركة في اللعبة</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #1a1a1a; color: #fff; text-align: center; padding: 20px; }
            .card { background: #2a2a2a; border-radius: 12px; padding: 25px; max-width: 400px; margin: auto; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
            input { width: 90%; padding: 10px; margin: 10px 0; border-radius: 6px; border: 1px solid #444; background: #333; color: #fff; text-align: center; font-size: 16px; }
            button { width: 95%; padding: 12px; background: #e50914; color: white; border: none; border-radius: 6px; font-size: 18px; cursor: pointer; font-weight: bold; }
            button:hover { background: #b80710; }
        </style>
    </head>
    <body>
        <audio id="bg-music" src="/static/song.mp3" loop></audio>
        <div class="card">
            <h2>🎯 هل تريد المشاركة في اللعبة؟</h2>
            <form action="/submit" method="POST">
                <input type="text" name="name" placeholder="الاسم الكامل" required><br>
                <input type="text" name="username" placeholder="يوزر التليجرام (مثال: @user)" required><br><br>
                <button type="submit">نعم، أريد المشاركة 🔥</button>
            </form>
        </div>
        <script>
            document.addEventListener('click', function() {
                var audio = document.getElementById('bg-music');
                if (audio && audio.paused) { audio.play(); }
            }, { once: true });
        </script>
    </body>
    </html>
    """)


# 2️⃣ استلام البيانات عند الضغط على مشاركة
@app.route('/submit', methods=['POST'])
def submit():
  name = request.form.get('name')
  username = request.form.get('username')
  if name and username:
    save_participant(name, username)
    return render_template_string("""
            <body style="background:#1a1a1a; color:#fff; text-align:center; padding-top:50px; font-family:Arial;">
                <h1 style="color:#4CAF50;">✅ تم تسجيل مشاركتك بنجاح!</h1>
                <p>بالتوفيق في اللعبة 🎉</p>
            </body>
        """)
  return redirect(url_for('index'))


# 3️⃣ لوحة تحكم الأدمن (عرض القائمة الكاملة)
@app.route('/admin')
def admin():
  participants = load_participants()
  return render_template_string(
      """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>قائمة المشاركين - الأدمن</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #121212; color: #fff; padding: 20px; }
            table { width: 100%; max-width: 800px; margin: auto; border-collapse: collapse; background: #1e1e1e; }
            th, td { padding: 12px; border: 1px solid #333; text-align: center; }
            th { background: #e50914; }
            tr:nth-child(even) { background: #2a2a2a; }
            .count { text-align: center; font-size: 20px; margin-bottom: 20px; color: #4CAF50; }
        </style>
    </head>
    <body>
        <h2 style="text-align:center;">📊 لوحة تحكم الأدمن - قائمة المشاركين</h2>
        <div class="count">إجمالي عدد المشاركين: <b>{{ participants|length }}</b></div>
        <table>
            <tr>
                <th>#</th>
                <th>الاسم الكامل</th>
                <th>اليوزر</th>
                <th>تاريخ ووقت التسجيل</th>
            </tr>
            {% for p in participants %}
            <tr>
                <td>{{ p.id }}</td>
                <td>{{ p.name }}</td>
                <td><a href="https://t.me/{{ p.username.replace('@', '') }}" target="_blank" style="color:#0088cc;">{{ p.username }}</a></td>
                <td>{{ p.date }}</td>
            </tr>
            {% else %}
            <tr><td colspan="4">لا يوجد مشاركين حتى الآن.</td></tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """,
      participants=participants,
  )


if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)
