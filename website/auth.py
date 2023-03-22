from flask import Blueprint

auth = Blueprint("auth", __name__)

@auth.route("/login")
def Login():
    return "<p>Login</p>"

@auth.route("/logout")
def Logout():
    return "<p>Logout</p>"

@auth.route("/sign-up")
def SignUp():
    return "<p>Sign Up</p>"