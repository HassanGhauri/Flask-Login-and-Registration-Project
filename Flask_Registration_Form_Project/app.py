import os
from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv("./.env")
app = Flask(__name__)
URL = os.environ['DB_URL']

app.config['SQLALCHEMY_DATABASE_URI'] = URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#required for database running
app.app_context().push()

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone_no = db.Column(db.String(100))
    password = db.Column(db.String(100))
 
 
    def __init__(self, name, email,phone_no,password):
        self.name = name
        self.email = email
        self.phone_no = phone_no
        self.password = password


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register" , methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        name = request.form["nm"]
        email = request.form["email"]
        phone_no = request.form["phno"]
        password = request.form["pswrd"]
        user = User(name=name,email=email,phone_no=phone_no,password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("home"))

@app.route("/user_detail")
def user_detail():
    users = User.query.all()
    return render_template("user_detail.html",users = users)

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    user = User.query.filter_by(id = id).first()
    if request.method =="GET":
        return render_template("update.html",user = user)
    
    if request.method == "POST":
        if user:
            db.session.delete(user)
            db.session.commit()

            name = request.form["nm"]
            email = request.form["email"]
            phone_no = request.form["phno"]
            password = request.form["pswrd"]
            user = User(name=name,email=email,phone_no=phone_no,password=password)
           
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user_detail"))

@app.route("/delete/<int:id>", methods=["GET","POST"])
def delete(id):
    user = User.query.filter_by(id = id).first()
    if request.method == "POST":
        if user:
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for("home"))

    return render_template("delete.html",user=user)



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)


