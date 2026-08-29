import os, base64
from flask import Flask, request, redirect
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

posts = []

HTML = """
<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{margin:0;font-family:Arial;background:#000;color:#fff}
.header{position:sticky;top:0;background:#000;border-bottom:1px solid #333;padding:12px;text-align:center;font-weight:bold;font-size:20px}
.story-bar{display:flex;overflow-x:auto;padding:10px;gap:15px;border-bottom:1px solid #222}
.story{text-align:center;font-size:12px}
.story img{width:60px;height:60px;border-radius:50%;border:2px solid #ff006a;object-fit:cover}
.upload-box{background:#111;border:1px solid #333;margin:10px;padding:15px;border-radius:10px}
.upload-box input, .upload-box textarea{width:100%;margin:5px 0;padding:10px;background:#222;color:#fff;border:1px solid #444;border-radius:8px}
.btn{background:#0095f6;color:#fff;border:0;padding:10px 20px;border-radius:8px;font-weight:bold;width:100%}
.post{border-bottom:1px solid #222;padding-bottom:10px}
.post img.post-img{width:100%;max-height:500px;object-fit:cover}
.post-head{padding:10px;display:flex;align-items:center;gap:10px}
.post-head img{width:32px;height:32px;border-radius:50%}
.post-text{padding:0 10px 10px}
</style></head><body>
<div class="header">IstaGranada 📸</div>
<div class="story-bar">
<div class="story"><img src="https://images.unsplash.com/photo-1539037116277-4db20889f2d4"><br>Alhambra</div>
<div class="story"><img src="https://images.unsplash.com/photo-1499856871958-5b9627545d1a"><br>Albaicin</div>
<div class="story"><img src="https://images.unsplash.com/photo-1516483638261-f4dbaf036963"><br>Sacromonte</div>
</div>
<div class="upload-box">
<h3>📸 Subir contenido nuevo</h3>
<form method="POST" enctype="multipart/form-data" action="/upload">
<input type="text" name="user" placeholder="Tu usuario (ej: cesar_grx)" required>
<textarea name="caption" placeholder="Escribe algo sobre Granada..."></textarea>
<input type="file" name="photo" accept="image/*" required>
<button class="btn">Publicar</button>
</form>
</div>
POSTS
</body></html>
"""

def render_posts():
    if not posts:
        return '<p style="text-align:center;color:#777;padding:20px">Aún no hay publicaciones. ¡Sube la primera!</p>'
    html=""
    for p in reversed(posts):
        html+=f'<div class="post"><div class="post-head"><img src="https://i.pravatar.cc/100?u={p["user"]}"><b>{p["user"]}</b></div><img class="post-img" src="{p["img"]}"><div class="post-text">{p["caption"]}<br><small style="color:#777">{p["time"]}</small></div></div>'
    return html

@app.route('/')
def home():
    return HTML.replace('POSTS', render_posts())

@app.route('/upload', methods=['POST'])
def upload():
    user = request.form.get('user','anon')
    caption = request.form.get('caption','')
    file = request.files.get('photo')
    if file:
        filename = datetime.now().strftime("%Y%m%d%H%M%S_") + file.filename
        path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(path)
        posts.append({"user":user,"caption":caption,"img":f"/{path}","time":datetime.now().strftime("%H:%M")})
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
