import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g


app = Flask(
    __name__,
    template_folder="Templates",
    static_folder="Styles",
    static_url_path="/static"
)

DATABASE = "../Back/ectoplase_bdr.db"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def change_db(query, args=()):
    cur = get_db().execute(query, args)
    get_db().commit()
    cur.close()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

@app.get("/connexion")
def connexion_get():
    return render_template("access.html", error=None)

@app.post("/connexion")
def connexion_post():
    role = request.form.get("role")
    email = request.form.get("email")
    password = request.form.get("password")

    if not role or not email or not password:
        return render_template("access.html", error="Champs manquants.")
    
    return f"Ok pour role={role}, email={email}"


@app.get("/")
def index():
    return redirect(url_for("connexion_get"))


@app.route("/eleves")
def eleves():
    return "Page élèves "

if __name__ == "__main__":
    app.run(debug=True)