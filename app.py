pkill nano; cd ~/Istagranada; rm -f app.py app.pp ista.db; cat > app.py << 'PY'
import os, base64
from flask import Flask, render_template_string, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
app=Flask(__name__)
app.secret_key="final-granada-2025"
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL','sqlite:///ista.db').replace("postgres://","postgresql://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
class User(db.Model):
 id=db.Column(db.Integer,primary_key=True)
 username=db.Column(db.String(80),unique=True)
 password=db.Column(db.String(200))
class Post(db.Model):
 id=db.Column(db.Integer,primary_key=True)
 image=db.Column(db.Text)
 user=db.Column(db.String(80))
 likes=db.Column(db.Integer,default=0)
 desc=db.Column(db.String(100),default="Granada")
class Message(db.Model):
 id=db.Column(db.Integer,primary_key=True)
 sender=db.Column(db.String(80))
 receiver=db.Column(db.String(80))
 text=db.Column(db.String(500))
with app.app_context(): db.create_all()
BASE="""<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1'><link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css'><style>body{background:black;color:white;margin:0;font-family:Arial;padding-bottom:60px}.top{position:fixed;top:0;width:100%;max-width:500px;left:50%;transform:translateX(-50%);background:black;display:flex;justify-content:space-between;align-items:center;padding:12px 15px;z-index:20;border-bottom:1px solid #111}.stories{display:flex;gap:14px;padding:60px 10px 10px;overflow-x:auto}.story{text-align:center;min-width:70px}.ring{width:66px;height:66px;border-radius:50%;background:linear-gradient(45deg,#feda75,#fa7e1e,#d62976,#962fbf,#4f5bd5);padding:2.5px}.ring img{width:100%;height:100%;border-radius:50%;border:3px solid black;object-fit:cover;background:#222}.post-head{display:flex;justify-content:space-between;padding:10px}.post-head .left{display:flex;gap:8px;align-items:center}.post-head img{width:32px;height:32px;border-radius:50%}.post img.main{width:100%}.actions{display:flex;justify-content:space-between;padding:10px 12px;font-size:24px}.actions div{display:flex;gap:16px}.nav{position:fixed;bottom:0;width:100%;max-width:500px;left:50%;transform:translateX(-50%);background:black;border-top:1px solid #222;display:flex;justify-content:space-around;padding:12px 0}.nav i{font-size:26px}.grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:2px}.grid img{width:100%;aspect-ratio:1;object-fit:cover}.btn{background:#0095f6;color:white;border:none;padding:12px;border-radius:8px;width:100%;font-weight:bold}input{background:#121212;border:1px solid #333;color:white;padding:12px;border-radius:8px;width:100%;box-sizing:border-box}</style></head><body><div style='max-width:500px;margin:auto;min-height:100vh'><div class='top'><a href='/upload_page' style='color:white'><i class='fa-solid fa-plus'></i></a><b>Para ti</b><a href='/notifications' style='color:white'><i class='fa-regular fa-heart'></i></a></div>{{content|safe}}<div class='nav'><a href='/' style='color:white'><i class='fa-solid fa-house'></i></a><a href='/live' style='color:#ff3040'><i class='fa-regular fa-circle-play'></i></a><a href='/chat' style='color:white'><i class='fa-regular fa-paper-plane'></i></a><a href='/search' style='color:white'><i class='fa-solid fa-magnifying-glass'></i></a><a href='/profile' style='color:white'><i class='fa-regular fa-user'></i></a></div></div></body></html>"""
@app.route('/')
def home():
 if 'user' not in session: return redirect('/login')
 posts=Post.query.order_by(Post.id.desc()).all()
 users=User.query.all()
 stories="<div class='stories'><div class='story'><div class='ring' style='background:#222'><img src='https://picsum.photos/100?random=me'></div><p>Tu historia</p></div>"
 for u in users:
  if u.username!=session['user']: stories+=f"<div class='story'><div class='ring'><img src='https://picsum.photos/100?random={u.id}'></div><p>{u.username[:8]}</p></div>"
 stories+="</div>"
 feed=""
 for p in posts: feed+=f"<div style='border-bottom:1px solid #111'><div class='post-head'><div class='left'><img src='https://picsum.photos/100?random={p.id}'><b>{p.user}</b></div><i class='fa-solid fa-ellipsis'></i></div><img class='main' src='{p.image}'><div class='actions'><div><a href='/like/{p.id}' style='color:white'><i class='fa-regular fa-heart'></i></a><i class='fa-regular fa-comment'></i><i class='fa-regular fa-paper-plane'></i></div><i class='fa-regular fa-bookmark'></i></div><div style='padding:0 12px 12px'><b>{p.likes} likes</b><br>{p.desc}</div></div>"
 if not posts: feed="<div style='text-align:center;padding:100px 20px;color:#666'>No hay fotos<br><br><a href='/upload_page' style='background:#0095f6;color:white;padding:12px 20px;border-radius:8px;text-decoration:none'>Subir foto</a></div>"
 return render_template_string(BASE,content=stories+feed)
@app.route('/upload_page')
def up_page():
 if 'user' not in session: return redirect('/login')
 return404: Not Found
