import requests, json
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return redirect("/")
    else:
        cpf = request.form.get("cpf")
        return render_template("home.html")
