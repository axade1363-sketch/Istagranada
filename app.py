from flask import Flask, request, redirect
import os, datetime
app = Flask(__name__)
posts = [{"user":"instagranada","image":"https://images.unsplash.com/photo-1539037116277-4db20889f2df?w=800","caption":"Bienvenidos a Instagranada - La red social de Granada 🔥","time":"Ahora"}]
HTML = """<style>.head{background:linear-gradient(90deg,orange,#e1306c,blue);padding:15px;text-align:center;font-weight:bold;font-size:22px;color:#fff}body{background:#000;color:#fff;font-family:sans-serif;margin:0}.box{background:#1a1a1a;margin:12px;padding:12px;border-radius:12px;border:1px solid #333}input,textarea{width:100%;padding:12px;margin:6px 0;border-radius:8px;background:#000;border:1px solid #333;color:#fff;box-sizing:border-box}.btn{background:#0095f6;color:#fff;border:0;padding:13px;border-radius:8px;width:100%;font-weight:bold}.post{border:1px solid #262626;margin:12px;border-radius:14px;overflow:hidden;background:#121212}.post img{width:100%}.info{padding:10px}</style><div class=head>INSTAGRANADA</div><div class=box><form method=POST><input name=user placeholder="Tu nombre" required><input name=image placeholder="URL de la foto" required><textarea name=caption placeholder="Que pasa en Granada?"></textarea><button class=btn>Publicar en Instagranada</button></form></div>{CONTENT}"""
@app.route("/",methods=["GET","POST"])
def home():
    if request.method=="POST":
        posts.insert(0,{"user":request.form.get("user"),"image":request.form.get("image"),"caption":request.form.get("caption"),"time":datetime.datetime.now().strftime("%d/%m %H:%M")})
        return redirect("/")
    content=""
    for p in posts: content+=f'<div class=post><img src="{p["image"]}"><div class=info><b>{p["user"]}</b> {p["caption"]}<br><small style="color:#888">{p["time"]}</small></div></div>'
    return HTML.replace("{CONTENT}",content)
@app.route("/admin")
def admin():
    html="<body style=background:#000;color:#0f0;font-family:monospace;padding:15px><h2>👑 ADMIN INSTAGRANADA</h2>Total posts: %d<br><br>"%len(posts)
    for i,p in enumerate(posts): html+=f"<div style=background:#111;padding:10px;margin:8px 0;border-radius:8px;border:1px solid #333>#{i} <b style=color:#fff>{p['user']}</b> - {p['time']}<br>{p['caption']}<br><small style=color:#888>{p['image'][:100]}</small></div>"
    return html+"<br><a href='/' style=color:#0095f6>Volver</a>"
if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
