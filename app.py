from flask import Flask, render_template, session, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import bcrypt
import os

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)

#decorator for unauthorized access
def authorize(func):
   def wrapper(*args, **kwargs):
      try:
         session['name'] != None
      except:
         flash("Vaše relace vypršela. Prosím přihlašte se.", "error")
         return redirect(url_for('login'))
      else:
        return func(*args, **kwargs)
   wrapper.__name__ = func.__name__
   return wrapper

@app.route("/")
def index():
   query = db.engine.execute('SELECT skola.nazev, mesto.nazev, obor.nazev, pocet_prijatych.pocet, pocet_prijatych.rok FROM mesto JOIN skola ON mesto.id=skola.mesto JOIN pocet_prijatych ON skola.id=pocet_prijatych.skola JOIN obor ON pocet_prijatych.obor=obor.id')
   return render_template("index.html", data=query)

@app.route('/addSchool', methods=["GET","POST"])
@authorize
def addSchool():
   if request.method == 'GET':
      return render_template('add_school.html')
   else:
      school = request.form['school']
      city = request.form['city']
      field = request.form['field']
      num_of_accepted = request.form['num_of_accepted']
      year = request.form['year']
      try:
         #TODO: insert
         #user = db.engine.execute(text("INSERT INTO saly (:school, :city, :field, :num_of_accepted, :year)"),school=school, city=city, field=field, num_of_accepted=num_of_accepted, year=year).first()
         flash("Ukládání proběhlo úspěšně.", "success")
         return redirect(url_for("index"))
      except Exception as e:
         flash("Při ukládání se vyskytla chyba.", "error")
         return redirect(url_for("index"))
      

@app.route("/map")
@authorize
def map():
    return render_template('map.html', api_key=os.getenv("MAPS_API_KEY"), lat="20.1115", long="40.1111")

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
            flash("Registrace proběhla úspěšně", "success")
            return redirect(url_for("index"))
         else:
            flash("Uživatel s tímto jménem již existuje", "error")
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
      flash("Jméno a heslo se neshodují", "error")
      return redirect(url_for("login"))
   else:
        return render_template('login.html')

@app.route('/logout')
def logout():
   session.clear()
   return redirect(url_for("login"))

if __name__ == "__main__":
   app.run(debug=True, threaded=True)