import os, base64
from flask import Flask, render_template_string, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "insta-final-2026"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///ista.db').replace("postgres://","postgresql://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(80), unique=True)
    password=db.Column(db.String(200))

class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    image=db.Column(db.Text)
    user=db.Column(db.String(80))
    likes=db.Column(db.Integer, default=0)
    desc=db.Column(db.String(200), default="Granada")

class Message(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    sender=db.Column(db.String(80))
    receiver=db.Column(db.String(80))
    text=db.Column(db.String(500))

with app.app_context():
    db.create_all()

BASE = """
<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1'>
<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css'>
<style>
body{background:black;color:white;margin:0;font-family:Arial;padding-bottom:60px}
.top{position:fixed;top:0;width:100%;max-width:500px;left:50%;transform:translateX(-50%);background:black;display:flex;justify-content:space-between;align-items:center;padding:12px 15px;z-index:20;box-sizing:border-box;border-bottom:1px solid #111}
.top b{font-size:20px}
.stories{display:flex;gap:14px;padding:60px 10px 10px 10px;overflow-x:auto;scrollbar-width:none}
.story{text-align:center;min-width:70px}
.ring{width:66px;height:66px;border-radius:50%;background:linear-gradient(45deg,#feda75,#fa7e1e,#d62976,#962fbf,#4f5bd5);padding:2.5px}
.ring img{width:100%;height:100%;border-radius:50%;border:3px solid black;object-fit:cover;background:#222}
.story p{font-size:12px;margin:6px 0 0}
.add{position:relative}
.add i{position:absolute;bottom:2px;right:0;background:#0095f6;border-radius:50%;padding:4px;font-size:12px;border:2px solid black}
.post-head{display:flex;justify-content:space-between;align-items:center;padding:10px}
.post-head .left{display:flex;align-items:center;gap:8px}
.post-head img{width:32px;height:32px;border-radius:50%;border:2px solid #d62976}
.post img.main{width:100%;height:auto;max-height:600px;object-fit:cover}
.actions{display:flex;justify-content:space-between;padding:10px 12px;font-size:24px}
.actions div{display:flex;gap:16px}
.badge{position:absolute;top:10px;right:10px;background:rgba(0,0,0,0.7);padding:6px 12px;border-radius:20px;font-size:13px}
.nav{position:fixed;bottom:0;width:100%;max-width:500px;left:50%;transform:translateX(-50%);background:black;border-top:1px solid #222;display:flex;justify-content:space-around;padding:12px 0;z-index:20}
.nav i{font-size:26px}
.nav img{width:28px;height:28px;border-radius:50%;border:2px solid white}
.grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:2px}
.grid img{width:100%;aspect-ratio:1;object-fit:cover}
.btn{background:#0095f6;color:white;border:none;padding:10px;border-radius:8px;width:100%;font-weight:bold}
input{background:#121212;border:1px solid #333;color:white;padding:12px;border-radius:8px;width:100%;box-sizing:border-box}
</style></head><body>
<div style='max-width:500px;margin:auto;position:relative;background:black;min-height:100vh'>

<div class='top'>
 <a href='/upload_page' style='color:white'><i class='fa-solid fa-plus' style='font-size:24px'></i></a>
 <b>Para ti <i class='fa-solid fa-chevron-down' style='font-size:14px'></i></b>
 <a href='/notifications' style='color:white'><i class='fa-regular fa-heart' style='font-size:24px'></i></a>
</div>

{{content|safe}}

<div class='nav'>
 <a href='/' style='color:white'><i class='fa-solid fa-house' style='color:{{ "white" if page=="home" else "#aaa" }}'></i></a>
 <a href='/live' style='color:white'><i class='fa-regular fa-circle-play' style='color:#ff3040'></i></a>
 <a href='/chat' style='color:white'><i class='fa-regular fa-paper-plane'></i></a>
 <a href='/search' style='color:white'><i class='fa-solid fa-magnifying-glass'></i></a>
 <a href='/profile'><img src='https://via.placeholder.com/100'></a>
</div>

</div>
</body></html>
"""

@app.route('/')
def home():
    if 'user' not in session: return redirect('/login')
    posts = Post.query.order_by(Post.id.desc()).all()
    users = User.query.all()

    stories = "<div class='stories'>"
    stories += "<div class='story add'><div class='ring' style='background:#222'><img src='https://via.placeholder.com/100'><i class='fa-solid fa-plus'></i></div><p>Tu historia</p></div>"
    for u in users[:8]:
        stories += f"<div class='story'><div class='ring'><img src='https://picsum.photos/100?random={u.id}'></div><p>{u.username[:9]}</p></div>"
    stories += "<div class='story'><div class='ring'><img src='https://picsum.photos/seed/fdezeli/100'></div><p>fdezeli</p></div>"
    stories += "<div class='story'><div class='ring'><img src='https://picsum.photos/seed/lgmrta/100'></div><p>lgmrta</p></div>"
    stories += "<div class='story'><div class='ring'><img src='https://picsum.photos/seed/say/100'></div><p>say.cruz</p></div>"
    stories += "</div>"

    feed = ""
    for i,p in enumerate(posts):
        feed += f"""
        <div style='border-bottom:1px solid #111;position:relative'>
         <div class='post-head'>
          <div class='left'><img src='https://picsum.photos/100?random={p.id}'><div><b>{p.user}</b><br><span style='font-size:12px;color:#aaa'>{p.desc}</span></div></div>
          <i class='fa-solid fa-ellipsis'></i>
         </div>
         <div style='position:relative'><img class='main' src='{p.image}'><div class='badge'>{i+1}/{len(posts)}</div></div>
         <div class='actions'><div><a href='/like/{p.id}' style='color:white'><i class='fa-regular fa-heart'></i></a><i class='fa-regular fa-comment'></i><i class='fa-regular fa-paper-plane'></i></div><i class='fa-regular fa-bookmark'></i></div>
         <div style='padding:0 12px 12px'><b>{p.likes} Me gusta</b><br><b>{p.user}</b> Granada 🔥</div>
        </div>
        """
    if not posts:
        feed = "<div style='text-align:center;padding:80px 20px;color:#666'><p>No hay fotos aún</p><a href='/upload_page' class='btn' style='text-decoration:none;display:inline-block;width:auto;padding:10px 30px'>Subir primera foto</a></div>"

    return render_template_string(BASE, content=stories+feed, page="home")

@app.route('/search')
def search():
    if 'user' not in session: return redirect('/login')
    posts = Post.query.order_by(Post.id.desc()).all()
    c = "<div style='padding:60px 0 0 0'><div style='padding:10px'><input placeholder='Buscar' id='s' onkeyup='filt()'></div><div class='grid' id='grid'>"
    for p in posts:
        c+= f"<img src='{p.image}'>"
    c+= "</div></div><script>function filt(){let v=document.getElementById('s').value.toLowerCase();document.querySelectorAll('.grid img').forEach(im=>{im.style.display=im.src.toLowerCase().includes(v)?'block':'none'})}</script>"
    return render_template_string(BASE, content=c, page="search")

@app.route('/profile')
def profile():
    if 'user' not in session: return redirect('/login')
    my = Post.query.filter_by(user=session['user']).order_by(Post.id.desc()).all()
    c = f"""
    <div style='padding:60px 15px 10px'>
     <div style='display:flex;gap:20px;align-items:center'><img src='https://via.placeholder.com/100' style='width:80px;height:80px;border-radius:50%'><div style='display:flex;gap:25px;text-align:center'><div><b>{len(my)}</b><br>posts</div><div><b>1.2k</b><br>seguidores</div><div><b>340</b><br>seguidos</div></div></div>
     <div style='margin:12px 0'><b>{session['user']}</b><br>📍 Granada<br>🔴 LIVE disponible</div>
     <div style='display:flex;gap:8px'><button class='btn' style='background:#262626;flex:1'>Editar perfil</button><button class='btn' style='background:#262626;flex:1'>Compartir</button></div>
    </div>
    <div style='display:flex;justify-content:space-around;border-top:1px solid #222;padding:10px'><i class='fa-solid fa-table-cells'></i><i class='fa-solid fa-clapperboard'></i><i class='fa-regular fa-id-badge'></i></div>
    <div class='grid'>{"".join([f"<img src='{p.image}'>" for p in my])}</div>
    <div style='padding:15px'><a href='/logout' style='color:#ff3040;text-decoration:none'>Cerrar sesión</a></div>
    """
    return render_template_string(BASE, content=c, page="profile")

@app.route('/upload_page')
def upload_page():
    if 'user' not in session: return redirect('/login')
    c = "<div style='padding:70px 15px'><h3><i class='fa-solid fa-plus'></i> Nueva publicación</h3><form action='/upload' method='post' enctype='multipart/form-data'><div style='border:2px dashed #333;padding:40px;text-align:center;border-radius:15px;margin:15px 0'><i class='fa-regular fa-image' style='font-size:40px'></i><br><br><input type='file' name='file' required></div><input name='desc' placeholder='Descripción... Camino de Santiago - Camino portugués' style='margin:10px 0'><button class='btn'>Compartir</button></form></div>"
    return render_template_string(BASE, content=c, page="home")

@app.route('/upload', methods=['POST'])
def upload():
    f=request.files['file']
    d=base64.b64encode(f.read()).decode()
    img=f"data:{f.mimetype};base64,{d}"
    db.session.add(Post(image=img, user=session['user'], desc=request.form.get('desc','Granada')))
    db.session.commit()
    return redirect('/')

@app.route('/like/<int:id>')
def like(id):
    p=Post.query.get(id)
    p.likes+=1
    db.session.commit()
    return redirect('/')

@app.route('/chat')
def chat_list():
    if 'user' not in session: return redirect('/login')
    users = User.query.filter(User.username != session['user']).all()
    c = "<div style='padding:60px 15px'><h3>Mensajes</h3>"
    for u in users:
        c+= f"<a href='/chat/{u.username}' style='color:white;text-decoration:none'><div style='display:flex;gap:10px;padding:12px 0;border-bottom:1px solid #111'><img src='https://picsum.photos/100?random={u.id}' style='width:50px;height:50px;border-radius:50%'><div><b>{u.username}</b><br><span style='color:#aaa'>Activo ahora</span></div></div></a>"
    c+="</div>"
    return render_template_string(BASE, content=c, page="chat")

@app.route('/chat/<username>', methods=['GET','POST'])
def chat(username):
    if 'user' not in session: return redirect('/login')
    if request.method=='POST':
        db.session.add(Message(sender=session['user'], receiver=username, text=request.form['text']))
        db.session.commit()
    msgs = Message.query.filter(((Message.sender==session['user']) & (Message.receiver==username)) | ((Message.sender==username) & (Message.receiver==session['user']))).all()
    c = f"<div style='padding:60px 15px 80px'><a href='/chat' style='color:white'><i class='fa-solid fa-arrow-left'></i> {username}</a><div style='margin-top:20px'>"
    for m in msgs:
        al = "right" if m.sender==session['user'] else "left"
        bg = "#0095f6" if m.sender==session['user'] else "#262626"
        c+= f"<div style='text-align:{al};margin:6px 0'><span style='background:{bg};padding:10px 15px;border-radius:20px;display:inline-block'>{m.text}</span></div>"
    c+= f"</div><form method='post' style='position:fixed;bottom:60px;left:50%;transform:translateX(-50%);width:100%;max-width:500px;display:flex;gap:5px;padding:10px;background:black'><input name='text' placeholder='Mensaje...' required style='flex:1'><button style='background:#0095f6;border:none;color:white;padding:12px 20px;border-radius:20px'>Enviar</button></form></div>"
    return render_template_string(BASE, content=c, page="chat")

LIVE = """
<div style='padding:70px 15px'>
<h3 style='text-align:center'>🔴 LIVE</h3>
<video id='myVideo' autoplay muted playsinline style='width:100%;height:400px;background:#111;border-radius:15px;object-fit:cover'></video><br><br>
<button id='start' class='btn' style='background:red'>Iniciar Live</button>
<button id='stop' class='btn' style='background:#333;display:none'>Terminar Live</button>
<p id='box' style='background:#111;padding:12px;border-radius:8px;display:none;word-break:break-all;margin-top:10px'></p>
<hr style='border:1px solid #222;margin:20px 0'>
<input id='peerId' placeholder='Pega ID de tu colega'><button id='join' class='btn' style='background:#00c853;margin-top:10px'>Ver su Live</button>
<video id='remote' autoplay playsinline style='width:100%;height:400px;background:#111;border-radius:15px;margin-top:10px;display:none;object-fit:cover'></video>
</div>
<script src='https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js'></script>
<script>
let peer=new Peer(),myStream,myId='';peer.on('open',id=>{myId=id});
document.getElementById('start').onclick=async()=>{
 myStream=await navigator.mediaDevices.getUserMedia({video:true,audio:true});
 document.getElementById('myVideo').srcObject=myStream;
 let b=document.getElementById('box');b.style.display='block';b.innerHTML='Tu ID: <b style=color:#ff3040;font-size:20px>'+myId+'</b><br>Compártelo!';
 document.getElementById('start').style.display='none';document.getElementById('stop').style.display='block';
}
document.getElementById('stop').onclick=()=>{myStream.getTracks().forEach(t=>t.stop());location.reload();}
peer.on('call',c=>{c.answer(myStream);});
document.getElementById('join').onclick=async()=>{
 let rid=document.getElementById('peerId').value;if(!rid)return alert('Pega ID');
 let s=await navigator.mediaDevices.getUserMedia({video:true,audio:true});
 let call=peer.call(rid,s);call.on('stream',ms=>{let v=document.getElementById('remote');v.style.display='block';v.srcObject=ms;});
}
</script>
"""

@app.route('/live')
def live():
    if 'user' not in session: return redirect('/login')
    return render_template_string(BASE, content=LIVE, page="home")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        u=User.query.filter_by(username=request.form['username']).first()
        if u and check_password_hash(u.password, request.form['password']):
            session['user']=u.username
            return redirect('/')
    c="<div style='padding:100px 20px;text-align:center'><h1 style='font-family:cursive;font-size:45px'>IstaGranada</h1><form method='post'><input name='username' placeholder='Usuario' required style='margin:8px 0'><input name='password' type='password' placeholder='Contraseña' required style='margin:8px 0'><button class='btn'>Entrar</button></form><br><a href='/register' style='color:#0095f6'>Registrarse</a></div>"
    return render_template_string(BASE, content=c, page="login")

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        u=User(username=request.form['username'], password=generate_password_hash(request.form['password']))
        db.session.add(u)
        db.session.commit()
        session['user']=u.username
        return redirect('/')
    c="<div style='padding:100px 20px;text-align:center'><h1 style='font-family:cursive;font-size:45px'>IstaGranada</h1><form method='post'><input name='username' placeholder='Usuario' required style='margin:8px 0'><input name='password' type='password' placeholder='Contraseña' required style='margin:8px 0'><button class='btn'>Crear cuenta</button></form></div>"
    return render_template_string(BASE, content=c, page="login")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/notifications')
def notif():
    c="<div style='padding:70px 15px'><h3>Notificaciones</h3><p style='color:#666'>❤️ A {0} le gustó tu foto</p><p style='color:#666'>👤 {0} te sigue</p></div>".format(session.get('user',''))
    return render_template_string(BASE, content=c, page="home")

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
