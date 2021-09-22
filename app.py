from flask import Flask, render_template, session, redirect, request
from flask_sqlalchemy import SQLAlchemy

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
      return "register page"
      #return render_template('register.html')
   else:
      name = request.form['name']
      password = request.form['password'].encode('utf-8')
      hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

      cur = mysql.connection.cursor()
      cur.execute("INSERT INTO uzivatele (uzivatelske_jmeno, heslo) VALUES (%s, %s)",(name,hash_password))
      mysql.connection.commit()
      session['name'] = name
      session['email'] = email
      return redirect(url_for("index"))

@app.route("/login", methods=["GET","POST"])
def login():
   if request.method == "POST":
      username = request.form['uzivatelske_jmeno']
      password = request.form['password'].encode('utf-8')

      cur = mysql.connection.cursor()
      cur.execute("SELECT * FROM uzivatele WHERE uzivatelske_jmeno=%s",(username,))
      user = cur.fetchone()
      cur.close()

      if len(user) > 0:
         if bcrypt.hashpw(password, user['heslo'].encode('utf-8')) == user['heslo'].encode('utf-8'):
            session['name'] = user['uzivatelske_jmeno']
            return render_template('index.html')
         else:
            return "Jméno a heslo se neshodují"
   else:
        return "Login page"
        #return render_template('login.html')

@app.route('/logout')
def logout():
   session.clear()
   return render_template("index.html")

if __name__ == "__main__":
   app.run(debug=True, threaded=True)