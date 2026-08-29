import os
from flask import Flask, render_template_string, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "istagranada-2024"
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
    likes=db.Column(db.Integer, default=0)

with app.app_context():
    db.create_all()

BASE = """
<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1'>
<style>body{background:black;color:white;margin:0;font-family:Arial}.header{display:flex;justify-content:space-between;padding:15px;border-bottom:1px solid #222}.logo{font-style:italic;font-size:26px}a{color:white;text-decoration:none;margin-left:10px}.btn{background:#0095f6;border:none;color:white;padding:12px;border-radius:8px;width:100%;font-weight:bold;margin-top:10px}.live{background:red;padding:6px 12px;border-radius:20px}.post{border:1px solid #222;margin:10px 0}.post img{width:100%}</style></head><body>
<div class='header'><div class='logo'>IstaGranada</div><div>{% if user %}<a href='/live' class='live'>LIVE</a><a href='/logout'>Salir</a>{% endif %}</div></div>
<div style='padding:15px;max-width:500px;margin:auto'>{{content|safe}}</div></body></html>
"""

LIVE_PAGE = """
<h2 style='text-align:center'>LIVE IstaGranada</h2>
<video id='myVideo' autoplay muted style='width:100%;background:#222;border-radius:10px;height:300px'></video><br><br>
<button id='start' class='btn' style='background:red'>Iniciar Directo</button>
<button id='stop' class='btn' style='background:#333;display:none'>Terminar</button>
<p id='box' style='background:#111;padding:10px;border-radius:8px;display:none'></p>
<hr><h3>Ver directo</h3>
<input id='peerId' placeholder='Pega ID del directo' style='width:100%;padding:12px;border-radius:8px;background:#111;color:white;border:1px solid #333'>
<button id='join' class='btn' style='background:#00c853'>Ver</button>
<video id='remote' autoplay style='width:100%;background:#222;border-radius:10px;height:300px;margin-top:10px;display:none'></video>
<script src='https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js'></script>
<script>
let peer=new Peer();let myStream;let myId='';peer.on('open',id=>{myId=id});
document.getElementById('start').onclick=async()=>{
 myStream=await navigator.mediaDevices.getUserMedia({video:true,audio:true});
 document.getElementById('myVideo').srcObject=myStream;
 let b=document.getElementById('box');b.style.display='block';b.innerHTML='Tu ID: <b style=color:#ff3040>'+myId+'</b>';
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

@app.route('/')
def index():
    if 'user' not in session:
        return redirect('/login')
    posts=Post.query.order_by(Post.id.desc()).all()
    html="<form action='/upload' method='post' enctype='multipart/form-data' style='border:1px solid #222;padding:15px;border-radius:10px'><input type='file' name='file' required><button class='btn'>Publicar</button></form>"
    for p in posts:
        html+=f"<div class='post'><img src='{p.image}'><div style='padding:10px'>❤️ {p.likes} <a href='/like/{p.id}'>Me gusta</a></div></div>"
    return render_template_string(BASE, user=session['user'], content=html)

@app.route('/live')
def live():
    if 'user' not in session:
        return redirect('/login')
    return render_template_string(BASE, user=session['user'], content=LIVE_PAGE)

@app.route('/upload', methods=['POST'])
def upload():
    import base64
    f=request.files['file']
    d=base64.b64encode(f.read()).decode()
    img=f"data:{f.mimetype};base64,{d}"
    db.session.add(Post(image=img))
    db.session.commit()
    return redirect('/')

@app.route('/like/<int:id>')
def like(id):
    p=Post.query.get(id)
    p.likes+=1
    db.session.commit()
    return redirect('/')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        u=User.query.filter_by(username=request.form['username']).first()
        if u and check_password_hash(u.password, request.form['password']):
            session['user']=u.username
            return redirect('/')
    c="<h2>Entrar</h2><form method='post'><input name='username' placeholder='Usuario' style='width:100%;padding:12px;margin:5px 0;border-radius:8px' required><input name='password' type='password' placeholder='Contrasena' style='width:100%;padding:12px;margin:5px 0;border-radius:8px' required><button class='btn'>Entrar</button></form><br><a href='/register'>Registrate</a>"
    return render_template_string(BASE, user=None, content=c)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        u=User(username=request.form['username'], password=generate_password_hash(request.form['password']))
        db.session.add(u)
        db.session.commit()
        session['user']=u.username
        return redirect('/')
    c="<h2>Registro</h2><form method='post'><input name='username' placeholder='Usuario' style='width:100%;padding:12px;margin:5px 0;border-radius:8px' required><input name='password' type='password' placeholder='Contrasena' style='width:100%;padding:12px;margin:5px 0;border-radius:8px' required><button class='btn'>Crear</button></form>"
    return render_template_string(BASE, user=None, content=c)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
