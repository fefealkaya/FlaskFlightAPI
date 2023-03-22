from flask import Blueprint, render_template

auth = Blueprint("auth", __name__)

@auth.route("/login")
def Login():
    return render_template("login.html", boolean=True)

@auth.route("/logout")
def Logout():
    return "<p>Logout</p>"

@auth.route("/sign-up")
def SignUp():
    return render_template("sign_up.html")