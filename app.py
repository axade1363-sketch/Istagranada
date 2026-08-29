import os, base64
from flask import Flask, render_template_string, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "istagranada-2024-full"
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
    created=db.Column(db.DateTime, default=datetime.utcnow)

class Message(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    sender=db.Column(db.String(80))
    receiver=db.Column(db.String(80))
    text=db.Column(db.String(500))
    created=db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

TEMPLATE = """
<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1, maximum-scale=1'>
<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'>
<style>
body{background:black;color:white;margin:0;font-family:Arial;padding-bottom:70px}
.header{position:fixed;top:0;width:100%;background:black;display:flex;justify-content:space-between;align-items:center;padding:12px 15px;border-bottom:1px solid #222;z-index:10;box-sizing:border-box}
.logo{font-family: 'Brush Script MT', cursive;font-size:28px}
.header i{font-size:22px;margin-left:18px}
.stories{display:flex;gap:12px;padding:80px 10px 10px 10px;overflow-x:auto;border-bottom:1px solid #222}
.story{text-align:center;min-width:65px}
.story .circle{width:60px;height:60px;border-radius:50%;background:linear-gradient(45deg,#f09433,#e6683c,#dc2743,#cc2366,#bc1888);padding:2px}
.story .circle img{width:100%;height:100%;border-radius:50%;border:2px solid black;background:#222;object-fit:cover}
.story p{font-size:11px;margin:5px 0 0}
.post{border-bottom:1px solid #222;padding-bottom:10px}
.post-head{display:flex;align-items:center;justify-content:space-between;padding:10px}
.post-head .u{display:flex;align-items:center;gap:8px;font-weight:bold}
.post-head img{width:30px;height:30px;border-radius:50%;background:#222}
.post img.main{width:100%;max-height:500px;object-fit:cover}
.actions{padding:10px;display:flex;gap:15px;font-size:24px}
.nav{position:fixed;bottom:0;width:100%;background:black;border-top:1px solid #222;display:flex;justify-content:space-around;padding:12px 0;z-index:10}
.nav i{font-size:24px}
.nav .active{color:white}
.live-btn{background:linear-gradient(45deg,red,#ff3040);padding:5px 10px;border-radius:6px;font-size:12px;font-weight:bold}
.btn{background:#0095f6;border:none;color:white;padding:12px;border-radius:8px;width:100%;font-weight:bold;margin-top:10px}
input{background:#121212;border:1px solid #333;color:white;padding:12px;border-radius:8px;width:100%;box-sizing:border-box}
.grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:2px}
.grid img{width:100%;aspect-ratio:1;object-fit:cover}
</style></head><body>

<div class='header'>
 <div class='logo'>IstaGranada</div>
 <div>
  <a href='/live' style='color:white;text-decoration:none'><span class='live-btn'><i class='fa-solid fa-video'></i> LIVE</span></a>
  <a href='/chat' style='color:white'><i class='fa-regular fa-paper-plane'></i></a>
 </div>
</div>

<div style='max-width:500px;margin:auto;background:black'>

{{content|safe}}

</div>

<div class='nav'>
 <a href='/' style='color:white'><i class='fa-solid fa-house {{ "active" if page=="home" }}'></i></a>
 <a href='/' style='color:white'><i class='fa-solid fa-magnifying-glass'></i></a>
 <a href='/upload_page' style='color:white'><i class='fa-regular fa-square-plus'></i></a>
 <a href='/live' style='color:white'><i class='fa-solid fa-clapperboard' style='color:#ff3040'></i></a>
 <a href='/profile' style='color:white'><i class='fa-regular fa-user {{ "active" if page=="profile" }}'></i></a>
</div>

</body></html>
"""

@app.route('/')
def home():
    if 'user' not in session: return redirect('/login')
    posts = Post.query.order_by(Post.id.desc()).all()
    users = User.query.all()
    
    stories_html = "<div class='stories'>"
    stories_html += f"<div class='story'><div class='circle'><img src='https://via.placeholder.com/60'></div><p>Tu historia</p></div>"
    for u in users[:10]:
        stories_html += f"<div class='story'><div class='circle'><img src='https://via.placeholder.com/60'></div><p>{u.username[:8]}</p></div>"
    stories_html += "</div>"

    feed = ""
    for p in posts:
        feed += f"""
        <div class='post'>
         <div class='post-head'><div class='u'><img src='https://via.placeholder.com/30'><span>{p.user}</span></div><i class='fa-solid fa-ellipsis'></i></div>
         <img class='main' src='{p.image}'>
         <div class='actions'><a href='/like/{p.id}' style='color:white'><i class='fa-regular fa-heart'></i></a><i class='fa-regular fa-comment'></i><i class='fa-regular fa-paper-plane'></i></div>
         <div style='padding:0 10px'><b>{p.likes} Me gusta</b><br>{p.user} <span style='color:#aaa'>Granada</span></div>
        </div>
        """

    content = stories_html + feed
    if not posts:
        content += "<div style='text-align:center;padding:50px;color:#666'><i class='fa-regular fa-images' style='font-size:50px'></i><p>No hay posts. ¡Sube el primero!</p><a href='/upload_page' class='btn' style='display:inline-block;width:auto;padding:10px 30px;text-decoration:none'>Subir foto</a></div>"

    return render_template_string(TEMPLATE, content=content, page="home")

@app.route('/upload_page')
def upload_page():
    if 'user' not in session: return redirect('/login')
    c = "<div style='padding:80px 15px'><h3>Nueva publicación</h3><form action='/upload' method='post' enctype='multipart/form-data'><input type='file' name='file' required style='padding:40px;border:2px dashed #333;text-align:center'><button class='btn'>Publicar ahora</button></form></div>"
    return render_template_string(TEMPLATE, content=c, page="home")

@app.route('/upload', methods=['POST'])
def upload():
    f=request.files['file']
    d=base64.b64encode(f.read()).decode()
    img=f"data:{f.mimetype};base64,{d}"
    db.session.add(Post(image=img, user=session['user']))
    db.session.commit()
    return redirect('/')

@app.route('/like/<int:id>')
def like(id):
    p=Post.query.get(id)
    p.likes+=1
    db.session.commit()
    return redirect('/')

@app.route('/profile')
def profile():
    if 'user' not in session: return redirect('/login')
    my_posts = Post.query.filter_by(user=session['user']).order_by(Post.id.desc()).all()
    c = f"""
    <div style='padding:70px 15px 10px 15px'>
     <div style='display:flex;align-items:center;gap:20px'><img src='https://via.placeholder.com/80' style='width:80px;height:80px;border-radius:50%'><div style='display:flex;gap:20px;text-align:center'><div><b>{len(my_posts)}</b><br>posts</div><div><b>0</b><br>seguidores</div><div><b>0</b><br>seguidos</div></div></div>
     <div style='margin-top:15px'><b>{session['user']}</b><br><span style='color:#aaa'>Granada, España</span></div>
     <button class='btn' style='background:#262626;margin-top:15px'>Editar perfil</button>
    </div>
    <div class='grid'>""" + "".join([f"<img src='{p.image}'>" for p in my_posts]) + "</div>"
    return render_template_string(TEMPLATE, content=c, page="profile")

@app.route('/chat')
def chat_list():
    if 'user' not in session: return redirect('/login')
    users = User.query.filter(User.username != session['user']).all()
    c = "<div style='padding:70px 15px'><h3>Mensajes</h3>"
    for u in users:
        c+= f"<a href='/chat/{u.username}' style='color:white;text-decoration:none'><div style='display:flex;align-items:center;gap:10px;padding:12px 0;border-bottom:1px solid #111'><img src='https://via.placeholder.com/50' style='width:50px;height:50px;border-radius:50%'><div><b>{u.username}</b><br><span style='color:#aaa;font-size:13px'>Activo ahora</span></div></div></a>"
    c += "</div>"
    return render_template_string(TEMPLATE, content=c, page="chat")

@app.route('/chat/<username>', methods=['GET','POST'])
def chat(username):
    if 'user' not in session: return redirect('/login')
    if request.method=='POST':
        db.session.add(Message(sender=session['user'], receiver=username, text=request.form['text']))
        db.session.commit()
    msgs = Message.query.filter(((Message.sender==session['user']) & (Message.receiver==username)) | ((Message.sender==username) & (Message.receiver==session['user']))).order_by(Message.id).all()
    c = f"<div style='padding:60px 15px 80px 15px'><div style='position:fixed;top:0;width:100%;max-width:500px;background:black;padding:15px;border-bottom:1px solid #222;left:50%;transform:translateX(-50%);box-sizing:border-box;z-index:5'><a href='/chat' style='color:white'><i class='fa-solid fa-arrow-left'></i></a> <b style='margin-left:15px'>{username}</b></div><div style='margin-top:20px'>"
    for m in msgs:
        align = "right" if m.sender==session['user'] else "left"
        bg = "#0095f6" if m.sender==session['user'] else "#262626"
        c+= f"<div style='text-align:{align};margin:8px 0'><span style='background:{bg};padding:10px 15px;border-radius:20px;display:inline-block;max-width:70%'>{m.text}</span></div>"
    c+= f"</div><form method='post' style='position:fixed;bottom:70px;width:100%;max-width:500px;left:50%;transform:translateX(-50%);display:flex;gap:5px;padding:10px;background:black;box-sizing:border-box'><input name='text' placeholder='Mensaje...' required style='flex:1'><button style='background:#0095f6;border:none;color:white;padding:12px 20px;border-radius:20px'><i class='fa-solid fa-paper-plane'></i></button></form></div>"
    return render_template_string(TEMPLATE, content=c, page="chat")

LIVE_HTML = """
<div style='padding:70px 15px'>
<h2 style='text-align:center'>🔴 LIVE IstaGranada</h2>
<video id='myVideo' autoplay muted playsinline style='width:100%;background:#222;border-radius:10px;height:380px;object-fit:cover'></video><br><br>
<button id='start' class='btn' style='background:red'><i class='fa-solid fa-video'></i> Iniciar Directo</button>
<button id='stop' class='btn' style='background:#333;display:none'>Terminar</button>
<p id='box' style='background:#111;padding:12px;border-radius:8px;display:none;word-break:break-all'></p>
<hr style='margin:20px 0;border:1px solid #222'>
<h3>Ver directo de amigo</h3>
<input id='peerId' placeholder='Pega ID del directo' style='margin-top:10px'>
<button id='join' class='btn' style='background:#00c853'><i class='fa-solid fa-eye'></i> Ver directo</button>
<video id='remote' autoplay playsinline style='width:100%;background:#222;border-radius:10px;height:380px;margin-top:10px;display:none;object-fit:cover'></video>
</div>
<script src='https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js'></script>
<script>
let peer=new Peer();let myStream;let myId='';peer.on('open',id=>{myId=id});
document.getElementById('start').onclick=async()=>{
 myStream=await navigator.mediaDevices.getUserMedia({video:true,audio:true});
 document.getElementById('myVideo').srcObject=myStream;
 let b=document.getElementById('box');b.style.display='block';b.innerHTML='Tu ID para compartir: <b style=color:#ff3040;font-size:18px>'+myId+'</b><br><br>¡Mándalo por WhatsApp a tus amigos!';
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
    return render_template_string(TEMPLATE, content=LIVE_HTML, page="home")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        u=User.query.filter_by(username=request.form['username']).first()
        if u and check_password_hash(u.password, request.form['password']):
            session['user']=u.username
            return redirect('/')
    c="<div style='padding:100px 20px;text-align:center'><h1 style='font-family:cursive;font-size:40px'>IstaGranada</h1><form method='post'><input name='username' placeholder='Usuario' required style='margin:8px 0'><input name='password' type='password' placeholder='Contraseña' required style='margin:8px 0'><button class='btn'>Entrar</button></form><br><a href='/register' style='color:#0095f6'>¿No tienes cuenta? Regístrate</a></div>"
    return render_template_string(TEMPLATE, content=c, page="login")

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        u=User(username=request.form['username'], password=generate_password_hash(request.form['password']))
        db.session.add(u)
        db.session.commit()
        session['user']=u.username
        return redirect('/')
    c="<div style='padding:100px 20px;text-align:center'><h1 style='font-family:cursive;font-size:40px'>IstaGranada</h1><form method='post'><input name='username' placeholder='Usuario' required style='margin:8px 0'><input name='password' type='password' placeholder='Contraseña' required style='margin:8px 0'><button class='btn'>Crear cuenta</button></form></div>"
    return render_template_string(TEMPLATE, content=c, page="login")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
