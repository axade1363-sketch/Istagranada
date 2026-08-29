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
posts=load(POSTS,[{"user":"instagranada","image":"https://images.unsplash.com/photo-1539037116277-4db20889f2df?w=800","caption":"Bienvenidos a Instagranada","time":"Ahora"}])
CSS="<style>body{background:#000;color:#fff;font-family:sans-serif;margin:0}.insta{max-width:380px;margin:50px auto;background:#121212;border:1px solid #333;border-radius:4px;padding:35px;text-align:center}.logo{font-family:cursive;font-size:38px}input{width:100%;padding:10px;margin:6px 0;background:#000;border:1px solid #333;border-radius:4px;color:#fff;box-sizing:border-box}.btn{width:100%;background:#0095f6;color:#fff;border:0;padding:9px;border-radius:8px;font-weight:bold;margin-top:10px}.head{background:#000;border-bottom:1px solid #222;padding:12px;text-align:center;position:sticky;top:0}.post{max-width:470px;margin:12px auto;background:#121212;border:1px solid #333;border-radius:8px;overflow:hidden}.post img{width:100%}.info{padding:10px;text-align:left} a{color:#0095f6;text-decoration:none}</style>"
@app.route("/", methods=["GET","POST"])
def home():
    global posts
    if "user" not in session: return redirect("/login")
    if request.method=="POST":
        img=request.form.get("image","").strip() or "https://images.unsplash.com/photo-1571003123894-1f0594d2b597?w=800"
        cap=request.form.get("caption","")[:500]
        posts.insert(0,{"user":session["user"],"image":img,"caption":cap,"time":datetime.datetime.now().strftime("%H:%M")})
        save(POSTS,posts)
        return redirect("/")
    h=f"{CSS}<div class=head><b>INSTAGRANADA</b> <span style=float:right><small>{session['user']}</small> <a href=/logout>Salir</a></span></div><div style=max-width:470px;margin:auto><div style=background:#121212;margin:10px;padding:12px;border:1px solid #333;border-radius:8px><form method=POST><input name=image placeholder='URL foto'><input name=caption placeholder='Que pasa en Granada?' required><button class=btn>Publicar</button></form></div>"
    for p in posts: h+=f'<div class=post><img src="{p["image"]}"><div class=info><b>{p["user"]}</b> {p["caption"]}</div></div>'
    return h+"</div>"
@app.route("/register", methods=["GET","POST"])
def register():
    global users
    if request.method=="POST":
        u=request.form.get("user","").strip().lower()[:20]
        e=request.form.get("email","").strip()
        p=hashlib.sha256(request.form.get("pwd","").encode()).hexdigest()
        ip=request.headers.get('X-Forwarded-For', request.remote_addr)
        if any(x["user"]==u for x in users): return f"{CSS}<div class=insta>Ya existe {u} <a href=/register>volver</a></div>"
        users.append({"user":u,"email":e,"pwd":p,"ip":ip,"fecha":datetime.datetime.now().strftime("%d/%m %H:%M:%S")})
        save(USERS,users); session["user"]=u; return redirect("/")
    return f"{CSS}<div class=insta><div class=logo>Instagranada</div><form method=POST><input name=user placeholder='Usuario' required><input name=email type=email placeholder='Email' required><input name=pwd type=password placeholder='Contraseña' required><button class=btn>Registrarse</button></form><br><div style=border:1px solid #333;padding:12px>¿Tienes cuenta? <a href=/login>Entra</a></div></div>"
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        u=request.form.get("user","").strip().lower()
        p=hashlib.sha256(request.form.get("pwd","").encode()).hexdigest()
        if any(x["user"]==u and x["pwd"]==p for x in users):
            session["user"]=u; return redirect("/")
        return f"{CSS}<div class=insta>Error<br><a href=/login>Intentar</a> | <a href=/forgot>Olvide pass</a></div>"
    return f"{CSS}<div class=insta><div class=logo>Instagranada</div><form method=POST><input name=user placeholder='Usuario' required><input name=pwd type=password placeholder='Contraseña' required><button class=btn>Entrar</button></form><div style=margin-top:15px><a href=/forgot style=font-size:12px>¿Olvidaste tu contraseña?</a></div><br><div style=border:1px solid #333;padding:12px>¿No tienes cuenta? <a href=/register>Regístrate</a></div></div>"
@app.route("/forgot", methods=["GET","POST"])
def forgot():
    global users
    if request.method=="POST":
        u=request.form.get("user","").strip().lower()
        e=request.form.get("email","").strip()
        np=request.form.get("newpwd","")
        for usr in users:
            if usr["user"]==u and usr["email"]==e:
                usr["pwd"]=hashlib.sha256(np.encode()).hexdigest()
                save(USERS,users)
                return f"{CSS}<div class=insta>✅ Contraseña cambiada<br><a href=/login class=btn>Login</a></div>"
        return f"{CSS}<div class=insta>No coincide <a href=/forgot>Volver</a></div>"
    return f"{CSS}<div class=insta><div class=logo>Recuperar</div><form method=POST><input name=user placeholder='Usuario' required><input name=email type=email placeholder='Email' required><input name=newpwd type=password placeholder='Nueva contraseña' required><button class=btn>Cambiar</button></form><br><a href=/login>Volver</a></div>"
@app.route("/logout")
def logout(): session.clear(); return redirect("/login")
@app.route("/admin")
def admin(): 
    h=f"{CSS}<div style=padding:15px;color:#0f0;font-family:monospace><h2 style=color:#fff>ADMIN - {len(users)} usuarios</h2><a href=/usuarios.json>📥 usuarios.json</a><hr>"
    for u in reversed(users): h+=f"<div style=background:#111;padding:10px;margin:5px 0;color:#fff>👤 {u['user']} | 📧 {u['email']}<br>🔒 hash:{u['pwd'][:20]}... | 🕒 {u['fecha']} | 🌐 {u['ip']}</div>"
    return h+"</div>"
@app.route("/usuarios.json")
def uj(): return app.response_class(json.dumps(users,indent=2), mimetype='application/json')
@app.route("/datos.json")
def dj(): return app.response_class(json.dumps(posts,indent=2), mimetype='application/json')
if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))

