import requests, json, os, configparser

from flask import Flask, render_template, request, redirect, session
from notion_api import make_headers, get_person_info, get_sessoes

# Initialize Application
app = Flask(__name__)

# Configure Environment Variables
config = configparser.ConfigParser()
config.read("config.ini")
for key, value in config["KEYS"].items():
    os.environ[key] = value

# Store Environment Variables
API = os.getenv("api_token")
PESSOAS = os.getenv("pessoas_database_id")
SESSOES = os.getenv("sessoes_database_id")

# Configure HTTP Request Headers
headers = make_headers(API)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return redirect("/")
    else:
        cpf = request.form.get("cpf")
        person_info = get_person_info(cpf, PESSOAS, headers)
        person_id = person_info["id"]
        person_name = person_info["name"]
        sessoes = get_sessoes(person_id, SESSOES, headers)
        return render_template("home.html", sessoes=sessoes, person_name=person_name)
