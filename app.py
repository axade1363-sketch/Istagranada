from flask import Flask, request, redirect
import json, os, datetime

app = Flask(__name__)
DB = "datos.json"

def cargar():
    if os.path.exists(DB):
        try:
            with open(DB,'r') as f:
                return json.load(f)
        except: pass
    return [{"user":"instagranada","image":"https://images.unsplash.com/photo-1539037116277-4db20889f2df?w=800","caption":"Bienvenidos a Instagranada 🔥","time":"Ahora","ip":"sistema"}]

def guardar(data):
    with open(DB,'w') as f:
        json.dump(data,f,indent=2)

posts = cargar()

BASE = """<style>body{background:#000;color:#fff;font-family:sans-serif;margin:0}.head{background:linear-gradient(90deg,orange,#e1306c,blue);padding:15px;text-align:center;font-weight:bold;font-size:22px}.box{background:#1a1a1a;margin:12px;padding:12px;border-radius:12px;border:1px solid #333}input,textarea{width:100%;padding:12px;margin:6px 0;border-radius:8px;background:#000;border:1px solid #333;color:#fff;box-sizing:border-box}.btn{background:#0095f6;color:#fff;border:0;padding:13px;border-radius:8px;width:100%;font-weight:bold}.post{border:1px solid #262626;margin:12px;border-radius:14px;overflow:hidden;background:#121212}.post img{width:100%}.info{padding:10px}</style><div class=head>INSTAGRANADA</div><div class=box><form method=POST><input name=user placeholder="Tu nombre" required><input name=image placeholder="URL de la foto - deja vacio para Alhambra"><textarea name=caption placeholder="Que pasa en Granada?" required></textarea><button class=btn>Publicar en Instagranada</button></form></div>{CONTENT}"""

@app.route("/", methods=["GET","POST"])
def home():
    global posts
    if request.method=="POST":
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        user = request.form.get("user","anonimo")[:30]
        img = request.form.get("image","").strip()
        if not img:
            img = "https://images.unsplash.com/photo-1571003123894-1f0594d2b597?w=800"
        caption = request.form.get("caption","")[:500]
        hora = datetime.datetime.now().strftime("%d/%m %H:%M:%S")
        posts.insert(0, {"user":user,"image":img,"caption":caption,"time":hora,"ip":ip})
        guardar(posts)
        return redirect("/")
    c=""
    for p in posts:
        c+=f'<div class=post><img src="{p["image"]}"><div class=info><b>{p["user"]}</b> {p["caption"]}<br><small style="color:#888">{p["time"]}</small></div></div>'
    return BASE.replace("{CONTENT}",c)

@app.route("/admin")
def admin():
    html=f"<body style=background:#000;color:#0f0;font-family:monospace;padding:15px><h2>👑 ADMIN INSTAGRANADA - GUARDADO PERMANENTE</h2>Total usuarios/posts: <b style=color:#fff>{len(posts)}</b><br>Archivo DB: {DB}<br>Hora: {datetime.datetime.now()}<br><br><a href='/datos.json' style=color:#0095f6>📥 DESCARGAR BASE
cat > app.py << 'PY'
from flask import Flask, request, redirect, session
import json, os, datetime, hashlib

app = Flask(__name__)
app.secret_key = "instagranada_secreto_2026"
USERS_DB = "usuarios.json"
POSTS_DB = "posts.json"

def cargar(f, defecto):
    if os.path.exists(f):
        try:
            with open(f,'r') as file: return json.load(file)
        except: pass
    return defecto

def guardar(f, data):
    with open(f,'w') as file: json.dump(data,file,indent=2)

users = cargar(USERS_DB, [])
posts = cargar(POSTS_DB, [{"user":"instagranada","image":"https://images.unsplash.com/photo-1539037116277-4db20889f2df?w=800","caption":"Bienvenidos a Instagranada 🔥","time":"Ahora"}])

BASE = """
<style>body{background:#000;color:#fff;font-family:sans-serif;margin:0}.head{background:linear-gradient(90deg,orange,#e1306c,blue);padding:15px;text-align:center;font-weight:bold;font-size:22px;position:sticky;top:0}.box{background:#1a1a1a;margin:12px;padding:12px;border-radius:12px;border:1px solid #333}input,textarea{width:100%;padding:12px;margin:6px 0;border-radius:8px;background:#000;border:1px solid #333;color:#fff;box-sizing:border-box}.btn{background:#0095f6;color:#fff;border:0;padding:13px;border-radius:8px;width:100%;font-weight:bold}.post{border:1px solid #262626;margin:12px;border-radius:14px;overflow:hidden;background:#121212}.post img{width:100%}.info{padding:10px} a{color:#0095f6;text-decoration:none}</style>
<div class=head><a href="/" style="color:#fff">INSTAGRANADA</a> <span style="float:right;font-size:12px"><a href="/register" style="color:#fff">Registro</a> | <a href="/admin" style="color:#fff">Admin</a></span></div>
{CONTENT}
"""

@app.route("/", methods=["GET","POST"])
def home():
    global posts
    if request.method=="POST":
        user = session.get("user", request.form.get("user","anon
curl -s https://istagranada.onrender.com/usuarios.json
cat > app.py << 'PY'
from flask import Flask, request, redirect, session
import json, os, datetime, hashlib
app = Flask(__name__)
app.secret_key = "granada2026"
USERS="usuarios.json"
POSTS="posts.json"

def load(f,d):
    if os.path.exists(f):
        try:
            with open(f,'r') as x: return json.load(x)
        except: pass
    return d
def save(f,d):
    with open(f,'w') as x: json.dump(d,x,indent=2)

users=load(USERS,[])
posts=load(POSTS,[{"user":"instagranada","image":"https://images.unsplash.com/photo-1539037116277-4db20889f2df?w=800","caption":"Bienvenidos a Instagranada 🔥 La red social de Granada","time":"Ahora"}])

CSS="<style>body{background:#000;color:#fff;font-family:-apple-system,BlinkMacSystemFont,sans-serif;margin:0}.insta{max-width:400px;margin:40px auto;background:#121212;border:1px solid #333;border-radius:3px;padding:30px 40px;text-align:center}.logo{font-family:Brush Script MT,cursive;font-size:40px;margin:10px 0}input{width:100%;padding:10px;margin:5px 0;background:#000;border:1px solid #333;border-radius:4px;color:#fff;box-sizing:border-box}.btn{width:100%;background:#0095f6;color:#fff;border:0;padding:8px;border-radius:8px;font-weight:bold;margin-top:10px}.head{background:#000;border-bottom:1px solid #333;padding:12px;text-align:center;position:sticky;top:0;z-index:10}.post{max-width:470px;margin:15px auto;background:#121212;border:1px solid #333;border-radius:8px;overflow:hidden}.post img{width:100%}.info{padding:10px;text-align:left} a{color:#0095f6;text-decoration:none}</style>"

@app.route("/", methods=["GET","POST"])
def home():
    global posts
    if "user" not in session:
        return redirect("/login")
    if request.method=="POST":
        img=request.form.get("image","").strip() or "https://images.unsplash.com/photo-1571003123894-1f0594d2b597?w=800"
        cap=request.form.get("caption","")[:500]
        hora=datetime.datetime.now().strftime("%H:%M")
        posts.insert(0,{"user":session["user"],"image":img,"caption":cap,"time":hora})
        save(POSTS,posts)
        return redirect("/")
    h=f"{CSS}<div class=head><b>INSTAGRANADA</b> <span style=float:right><small>{session['user']}</small> | <a href=/logout>Salir</a> | <a href=/admin>Admin</a></span></div><div style=max-width:470px;margin:auto><div style=background:#121212;margin:12px;padding:12px;border:1px solid #333;border-radius:8px><form method=POST><input name=image placeholder='URL foto'><input name=caption placeholder='¿Qué pasa en Granada?' required><button class=btn>Publicar</button></form></div>"
    for p in posts: h+=f'<div class=post><img src="{p["image"]}"><div class=info><b>{p["user"]}</b> {p["caption"]}<br><small style=color:#888>{p["time"]}</small></div></div>'
    return h+"</div>"

@app.route("/register", methods=["GET","POST"])
def register():
    global users
    if request.method=="POST":
        u=request.form.get("user","").strip().lower()[:20]
        e=request.form.get("email","").strip()
        p=hashlib.sha256(request.form.get("pwd","").encode()).hexdigest()
        ip=request.headers.get('X-Forwarded-For', request.remote_addr)
        if any(x["user"]==u for x in users): return f"{CSS}<div class=insta>Usuario {u} ya existe <br><br><a href=/register>Volver</a></div>"
        users.append({"user":u,"email":e,"pwd":p,"ip":ip,"fecha":datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
        save(USERS,users)
        session["user"]=u
        return redirect("/")
    return f"{CSS}<div class=insta><div class=logo>Instagranada</div><p style=color:#888>Regístrate para ver fotos de Granada</p><form method=POST><input name=user placeholder='Nombre de usuario' required><input name=email type=email placeholder='Correo electrónico' required><input name=pwd type=password placeholder='Contraseña' required><button class=btn>Registrarse</button></form><br><div style=border:1px solid #333;padding:15px>¿Tienes cuenta? <a href=/login>Inicia sesión</a></div></div>"

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        u=request.form.get("user","").strip().lower()
        p=hashlib.sha256(request.form.get("pwd","").encode()).hexdigest()
        if any(x["user"]==u and x["pwd"]==p for x in users):
            session["user"]=u
            return redirect("/")
        return f"{CSS}<div class=insta>Contraseña incorrecta <br><br><a href=/login>Volver</a></div>"
    return f"{CSS}<div class=insta><div class=logo>Instagranada</div><form method=POST><input name=user placeholder='Nombre de usuario' required><input name=pwd type=password placeholder='Contraseña' required><button class=btn>Iniciar sesión</button></form><br><div style=border:1px solid #333;padding:15px>¿No tienes cuenta? <a href=/register>Regístrate</a></div></div>"

@app.route("/logout")
def logout(): session.clear(); return redirect("/login")

@app.route("/admin")
def admin():
    html=f"{CSS}<div style=padding:15px;font-family:monospace;color:#0f0><h2 style=color:#fff>👑 ADMIN - {len(users)} USUARIOS CON CONTRASEÑA</h2><a href=/usuarios.json>📥 Descargar usuarios.json</a> | <a href=/datos.json>📥 Posts</a><hr>"
    for u in reversed(users): html+=f"<div style=background:#111;padding:10px;margin:6px 0;border:1px solid #333;color:#fff>👤 <b>{u['user']}</b> | 📧 {u['email']}<br>🔑 hash: {u['pwd'][:15]}... | 🌐 {u['ip']}<br>🕒 {u['fecha']}</div>"
    return html+"</div>"

@app.route("/usuarios.json")
def uj(): return app.response_class(json.dumps(users,indent=2), mimetype='application/json')
@app.route("/datos.json")
def dj(): return app.response_class(json.dumps(posts,indent=2), mimetype='application/json')

if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
