from flask import Flask, render_template_string, request, redirect
import os, datetime
app = Flask(__name__)
posts=[{"user":"instagranada","image":"https://images.unsplash.com/photo-1539037116277-4db20889f2d4?w=800","caption":"Bienvenidos a Instagranada - La red social de Granada 🔥","time":"Ahora"}]
HTML="""
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Instagranada</title>
<style>
body{background:#000;color:#fff;font-family:sans-serif;margin:0}
.head{background:linear-gradient(90deg,#feda75,#fa7e1e,#d62976,#962fbf,#4f5bd5);padding:15px;text-align:center;font-weight:900;font-size:24px}
.box{border:1px solid #262626;margin:12px;padding:12px;border-radius:14px;background:#121212}
.post{border:1px solid #262626;margin:12px;border-radius:14px;overflow:hidden;background:#121212}
.post img{width:100%} .info{padding:10px}
input,textarea{width:100%;padding:12px;margin:6px 0;border-radius:8px;background:#000;border:1px solid #333;color:#fff;box-sizing:border-box}
.btn{background:#0095f6;color:#fff;border:0;padding:13px;border-radius:8px;width:100%;font-weight:bold}
</style></head><body>
<div class=head>INSTAGRANADA</div>
<div class=box><form method=POST><input name=user placeholder="Tu nombre" required><input name=image placeholder="URL de la foto" required><textarea name=caption placeholder="Que pasa en Granada?"></textarea><button class=btn>Publicar en Instagranada</button></form></div>
{% for p in posts[::-1] %}<div class=post><img src="{{p.image}}"><div class=info><b>{{p.user}}</b> {{p.caption}}<br><small style=color:#888>{{p.time}}</small></div></div>{% endfor %}
</body></html>
"""
@app.route("/",methods=["GET","POST"])
def home():
 if request.method=="POST":
  posts.append({"user":request.form.get("user"),"image":request.form.get("image"),"caption":request.form.get("caption"),"time":datetime.datetime.now().strftime("%d/%m %H:%M")})
  return redirect("/")
 return render_template_string(HTML,posts=posts)
if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
