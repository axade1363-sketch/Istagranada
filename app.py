import json, os, datetime, hashlib
from flask import Flask, request, redirect, session
app = Flask(__name__)
app.secret_key = "granada2026"
USERS="usuarios.json"
POSTS="posts.json"
CLAVE_ADMIN="GranadaPro2026"
def load(f,d):
    if os.path.exists(f):
        try:
            with open(f,'r') as x: return json.load(x)
        except: pass
    return d
def save(f,d):
    with open(f,'w') as x: json.dump(d,x,indent=2)
users=load(USERS,[])
posts=load(POSTS,[{"user":"instagranada","img":"https://images.unsplash.com/photo-1533105079780-92b9be482077?w=800","text":"Bienvenidos a Instagranada 🔥"}])
CSS="<style>body{background:#000;color:#fff;font-family:Arial;margin:0} .box{max-width:400px;margin:30px auto;background:#111;padding:20px;border:1px solid #333} input{width:100%;padding:12px;margin:8px 0;background:#222;border:1px solid #444;color:#fff} button{width:100%;padding:12px;background:#0095f6;color:#fff;border:0;font-weight:bold} a{color:#0095f6}</style>"
@app.route("/usuarios.json")
def ver_json():
    if request.args.get("clave") != CLAVE_ADMIN:
        return "403 Acceso denegado - pon ?clave=GranadaPro2026", 403
    return open(USERS).read() if os.path.exists(USERS) else "[]", 200, {'Content-Type':'application/json'}
@app.route("/admin")
def admin():
    if request.args.get("clave") != CLAVE_ADMIN:
        return "<h1>403</h1> Solo admin con clave", 403
    u=load(USERS,[])
    h=f"<h1>Panel Admin ({len(u)} usuarios)</h1><a href='/'>Volver</a><hr>"
    for i in u[::-1]:
        h+=f"<div style='background:#111;margin:10px;padding:10px;border:1px solid #333'><b>{i.get('user')}</b> - {i.get('email')}<br>IP:{i.get('ip')} - {i.get('fecha')}<br>Hash:{i.get('pwd')[:25]}...</div>"
    return h
@app.route("/", methods=["GET","POST"])
def home():
    global posts
    if "user" not in session: return redirect("/login")
    if request.method=="POST":
        img=request.form.get("img","").strip()
        text=request.form.get("text","").strip()
        if not img: img="https://images.unsplash.com/photo-1533105079780-92b9be482077?w=800"
        posts.insert(0,{"user":session["user"],"img":img,"text":text})
        save(POSTS,posts)
    html=CSS+f"<div class='box'><h2>Feed - {session['user']} <a href='/logout'>Salir</a></h2><form method=post><input name=img placeholder='URL foto'><input name=text placeholder='Que pasa en Granada?'><button>Publicar</button></form><hr>"
    for p in posts:
        html+=f"<div style='border:1px solid #333;margin:15px 0'><b>{p['user']}</b><br><img src='{p['img']}' style='width:100%'><p>{p['text']}</p></div>"
    html+=f"<p><a href='/admin?clave={CLAVE_ADMIN}'>Panel Admin (solo tu)</a></p></div>"
    return html
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        u=request.form.get("user","").strip(); p=request.form.get("pwd","")
        h=hashlib.sha256(p.encode()).hexdigest()
        for x in load(USERS,[]):
            if x["user"]==u and x["pwd"]==h:
                session["user"]=u
                return redirect("/")
        return CSS+"<div class='box'><h3>Error login</h3><a href='/login'>Volver</a></div>"
    return CSS+"<div class='box'><h2>Instagranada</h2><form method=post><input name=user placeholder=Usuario><input name=pwd type=password placeholder=Contraseña><button>Entrar</button></form><a href='/register'>Registrarse</a></div>"
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method=="POST":
        u=request.form.get("user","").strip(); e=request.form.get("email","").strip(); p=request.form.get("pwd","")
        if not u or not p: return "Falta dato"
        us=load(USERS,[])
        if any(x["user"]==u for x in us): return "Usuario existe"
        us.append({"user":u,"email":e,"pwd":hashlib.sha256(p.encode()).hexdigest(),"ip":request.headers.get('X-Forwarded-For',request.remote_addr),"fecha":datetime.datetime.now().strftime("%d/%m %H:%M:%S")})
        save(USERS,us)
        return redirect("/login")
    return CSS+"<div class='box'><h2>Registro</h2><form method=post><input name=user placeholder=Usuario><input name=email placeholder=Email><input name=pwd type=password placeholder=Pass><button>Registrar</button></form><a href='/login'>Login</a></div>"
@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect("/login")
if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))
