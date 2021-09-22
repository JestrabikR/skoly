from flask import Flask, render_template, session, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import bcrypt

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)

@app.route("/")
def index():
    query = db.engine.execute('SELECT skola.nazev, mesto.nazev, obor.nazev, pocet_prijatych.pocet, pocet_prijatych.rok FROM mesto JOIN skola ON mesto.id=skola.mesto JOIN pocet_prijatych ON skola.id=pocet_prijatych.skola JOIN obor ON pocet_prijatych.obor=obor.id')
    return render_template("index.html", data=query)

@app.route("/map")
def map():
    return "map"

@app.route('/register', methods=["GET","POST"])
def register():
   if request.method == 'GET':
      return render_template('register.html')
   else:
      username = request.form['username']
      password = request.form['password'].encode('utf-8')
      hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
      try:
         user = db.engine.execute(text("SELECT * FROM uzivatele WHERE uzivatelske_jmeno=:username"),username=username,).first()
         if user == None:
            db.engine.execute("INSERT INTO uzivatele (uzivatelske_jmeno, heslo) VALUES (%s, %s)",(username,hash_password))
            session['name'] = username
            return redirect(url_for("index"))
         else:
            flash("Uživatel s tímto jménem již existuje")
            return redirect(url_for("register"))
      except Exception as e:
         print(e)
         return "chyba"
      

@app.route("/login", methods=["GET","POST"])
def login():
   if request.method == "POST":
      username = request.form['username']
      password = request.form['password'].encode('utf-8')

      user = db.engine.execute(text("SELECT * FROM uzivatele WHERE uzivatelske_jmeno=:username"),username=username,).first()

      if user != None:
         if bcrypt.hashpw(password, user[2].encode('utf-8')) == user[2].encode('utf-8'):
            session['name'] = user[1]
            return redirect(url_for("index"))
      #Login fail
      flash("Jméno a heslo se neshodují")
      return redirect(url_for("login"))
   else:
        return render_template('login.html')

@app.route('/logout')
def logout():
   session.clear()
   return redirect(url_for("login"))

if __name__ == "__main__":
   app.run(debug=True, threaded=True)