import os, base64
from flask import Flask, render_template_string, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "insta-limpio-2026"
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
    desc=db.Column(db.String(100), default="Granada")
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
.stories{display:flex;gap:14px;padding:60px 10px 10px;overflow-x:auto}
.story{text-align:center;min-width:70px}.ring{width:66px;height:66px;border-radius:50%;background:linear-gradient(45deg,#feda75,#fa7e1e,#d62976,#962fbf,#4f5bd5);padding:2.5px}
.ring img{width:100%;height:100%;border-radius:50%;border:3px solid black;object-fit:cover;background:#222}
.post-head{display:flex;justify-content:space-between;padding:10px}.post-head .left{display:flex;gap:8px;align-items:center}
.post-head img{width:32px;height:32px;border-radius:50%}.post img.main{width:100%;object-fit:cover}
.actions{display:flex;justify-content:space-between;padding:10px 12px;font-size:24px}.actions div{display:flex;gap:16px}
.nav{position:fixed;bottom:0;width:100%;max-width:500px;left:50%;transform:translateX(-50%);background:black;border-top:1px solid #222;display:flex;justify-content:space-around;padding:12px 0;z-index:20}
.nav i{font-size:26px}.grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:2px}.grid img{width:100%;aspect-ratio:1;object-fit:cover}
.btn{background:#0095f6;color:white;border:none;padding:12px;border-radius:8px;width:100%;font-weight:bold}
input{background:#121212;border:1px solid #333;color:white;padding:12px;border-radius:8px;width:100%;box-sizing:border-box}
</style></head><body><div style='max-width:500px;margin:auto;background:black;min-height:100vh'>
<div class='top'><a href='/upload_page' style='color:white'><i class='fa-solid fa-plus' style='font-size:24px'></i></a><b>Para ti <i class='fa-solid fa-chevron-down' style='font-size:14px'></i></b><a href='/reset' style='color:#ff3040;font-size:12px;text-decoration:none'>BORRAR TODO</a></div>
{{content|safe}}
<div class='nav'>
 <a href='/' style='color:white'><i class='fa-solid fa-house'></i></a>
 <a href='/live' style='color:#ff3040'><i class='fa-regular fa-circle-play'></i></a>
 <a href='/chat' style='color:white'><i class='fa-regular fa-paper-plane'></i></a>
 <a href='/search' style='color:white'><i class='fa-solid fa-magnifying-glass'></i></a>
 <a href='/profile' style='color:white'><i class='fa-regular fa-user'></i></a>
</div></div></body></html>
"""

@app.route('/')
def home():
    if 'user' not in session: return redirect('/login')
    posts=Post.query.order_by(Post.id.desc()).all()
    users=User.query.all()
    stories="<div class='stories'>"
    stories+=f"<div class='story'><div class='ring' style='background:#222'><img src='https://picsum.photos/100?random={session['user']}'></div><p>Tu historia</p></div>"
    for u in users:
        if u.username!=session['user']:
            stories+=f"<div class='story'><div class='ring'><img src='https://picsum.photos/100?random={u.id}'></div><p>{u.username[:9]}</p></div>"
    stories+="</div>"
    feed=""
    for p in posts:
        feed+=f"<div style='border-bottom:1px solid #111'><div class='post-head'><div class='left'><img src='https://picsum.photos/100?random={p.id}'><b>{p.user}</b></div><i class='fa-solid fa-ellipsis'></i></div><img class='main' src='{p.image}'><div class='actions'><div><a href='/like/{p.id}' style='color:white'><i class='fa-regular fa-heart'></i></a><i class='fa-regular fa-comment'></i><i class='fa-regular fa-paper-plane'></i></div><i class='fa-regular fa-bookmark'></i></div><div style='padding:0 12px 12px'><b>{p.likes} likes</b><br>{p.desc}</div></div>"
    if not posts:
        feed="<div style='text-align:center;padding:100px 20px;color:#666'>No hay fotos aún<br><br><a href='/upload_page' style='background:#0095f6;color:white;padding:12px 25px;border-radius:8px;text-decoration:none;font-weight:bold'>Subir primera foto</a></div>"
    return render_template_string(BASE, content=stories+feed)

@app.route('/reset')
def reset():
    db.drop_all()
    db.create_all()
    session.clear()
    return redirect('/login')

@app.route('/upload_page')
def up_page():
    if 'user' not in session: return redirect('/login')
    c="<div style='padding:70px 15px'><h3>Nueva publicación</h3><form action='/upload' method='post' enctype='multipart/form-data'><input type='file' name='file' required style='padding:30px;border:2px dashed #333'><input name='desc' placeholder='Descripción' style='margin:10px 0'><button class='btn'>Compartir</button></form></div>"
    return render_template_string(BASE, content=c)

@app.route('/upload', methods=['POST'])
def upload():
    f=request.files['file'];img=f"data:{f.mimetype};base64,{base64.b64encode(f.read()).decode()}"
    db.session.add(Post(image=img, user=session['user'], desc=request.form.get('desc','Granada')));db.session.commit()
    return redirect('/')

@app.route('/like/<int:id>')
def like(id):
    p=Post.query.get(id);p.likes+=1;db.session.commit()
    return redirect('/')

@app.route('/search')
def search():
    c="<div style='padding:70px 15px'><input placeholder='Buscar usuario'><div style='margin-top:20px;color:#666'>Busca a alguien por nombre</div></div>"
    return render_template_string(BASE, content=c)

@app.route('/profile')
def profile():
    if 'user' not in session: return redirect('/login')
    my=Post.query.filter_by(user=session['user']).all()
    c=f"<div style='padding:60px 15px'><b>{session['user']}</b> - {len(my)} posts<div class='grid' style='margin-top:15px'>"+ "".join([f"<img src='{p.image}'>" for p in my])+"</div><br><a href='/logout' style='color:#ff3040'>Salir</a> | <a href='/reset' style='color:#ff3040'>Borrar todo</a></div>"
    return render_template_string(BASE, content=c)

@app.route('/chat')
def chat_list():
    if 'user' not in session: return redirect('/login')
    users=User.query.filter(User.username!=session['user']).all()
    c="<div style='padding:70px 15px'><h3>Mensajes</h3>"
    for u in users: c+=f"<a href='/chat/{u.username}' style='color:white;text-decoration:none'><div style='padding:12px 0;border-bottom:1px solid #111'><b>{u.username}</b></div></a>"
    c+="</div>"
    return render_template_string(BASE, content=c)

@app.route('/chat/<username>', methods=['GET','POST'])
def chat(username):
    if 'user' not in session: return redirect('/login')
    if request.method=='POST': db.session.add(Message(sender=session['user'], receiver=username, text=request.form['text']));db.session.commit()
    msgs=Message.query.filter(((Message.sender==session['user']) & (Message.receiver==username)) | ((Message.sender==username) & (Message.receiver==session['user']))).all()
    c=f"<div style='padding:70px 15px'><a href='/chat' style='color:white'>← {username}</a><div style='margin-top:15px'>"
    for m in msgs: c+=f"<div style='margin:6px 0'><b>{m.sender}:</b> {m.text}</div>"
    c+=f"</div><form method='post' style='position:fixed;bottom:60px;left:50%;transform:translateX(-50%);width:100%;max-width:500px;display:flex;padding:10px;background:black'><input name='text' required placeholder='Mensaje...'><button class='btn' style='width:auto;margin-left:5px'>Enviar</button></form></div>"
    return render_template_string(BASE, content=c)

@app.route('/live')
def live():
    c="""
    <div style='padding:70px 15px'><video id='myVideo' autoplay muted playsinline style='width:100%;height:350px;background:#111;border-radius:15px'></video><br><br>
    <button id='start' class='btn' style='background:red'>Iniciar Live</button><button id='stop' class='btn' style='background:#333;display:none'>Terminar</button>
    <p id='box' style='background:#111;padding:10px;border-radius:8px;display:none;word-break:break-all'></p><hr style='border:1px solid #222;margin:20px 0'>
    <input id='peerId' placeholder='ID del directo'><button id='join' class='btn' style='background:#00c853;margin-top:10px'>Ver Live</button><video id='remote' autoplay playsinline style='width:100%;height:350px;background:#111;border-radius:15px;margin-top:10px;display:none'></video></div>
    <script src='https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js'></script><script>
    let peer=new Peer(),myStream,myId='';peer.on('open',id=>{myId=id});
    document.getElementById('start').onclick=async()=>{myStream=await navigator.mediaDevices.getUserMedia({video:true,audio:true});document.getElementById('myVideo').srcObject=myStream;let b=document.getElementById('box');b.style.display='block';b.innerHTML='Tu ID: <b style=color:#ff3040>'+myId+'</b>';document.getElementById('start').style.display='none';document.getElementById('stop').style.display='block';}
    document.getElementById('stop').onclick=()=>{myStream.getTracks().forEach(t=>t.stop());location.reload();};peer.on('call',c=>{c.answer(myStream);});
    document.getElementById('join').onclick=async()=>{let rid=document.getElementById('peerId').value;let s=await navigator.mediaDevices.getUserMedia({video:true,audio:true});let call=peer.call(rid,s);call.on('stream',ms=>{let v=document.getElementById('remote');v.style.display='block';v.srcObject=ms;});}
    </script>"""
    return render_template_string(BASE, content=c)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        u=User.query.filter_by(username=request.form['username']).first()
        if u and check_password_hash(u.password, request.form['password']): session['user']=u.username;return redirect('/')
    c="<div style='padding:100px 20px;text-align:center'><h1 style='font-family:cursive;font-size:45px'>IstaGranada</h1><form method='post'><input name='username' placeholder='Usuario' required style='margin:8px 0'><input name='password' type='password' placeholder='Contraseña' required style='margin:8px 0'><button class='btn'>Entrar</button></form><br><a href='/register' style='color:#0095f6'>Crear cuenta nueva</a></div>"
    return render_template_string(BASE, content=c)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        u=User(username=request.form['username'], password=generate_password_hash(request.form['password']));db.session.add(u);db.session.commit();session['user']=u.username;return redirect('/')
    c="<div style='padding:100px 20px;text-align:center'><h1>IstaGranada</h1><form method='post'><input name='username' placeholder='Usuario' required><input name='password' type='password' placeholder='Contraseña' required style='margin:10px 0'><button class='btn'>Crear</button></form></div>"
    return render_template_string(BASE, content=c)

@app.route('/logout')
def logout(): session.clear();return redirect('/login')

if __name__=='__main__': app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
