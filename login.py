import os
from datetime import datetime
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

def write_to_file(filename, data):
    """
    Handle the process of writing data to a file
    """
    with open(filename, "a") as file:
        file.writelines(data)

def save_user(username):
    """
    Add usernames to the `usernames.txt` list
    """
    write_to_file("data/usernames.txt", "{0}\n".format(username))

@app.route('/', methods=["GET", "POST"])
def index():
    """
    Making page with instructions
    #Handle POST
    """
    if request.method == "POST":
        write_to_file("data/usernames.txt", request.form["username"] + "\n")
        print(request.form)
        return redirect(request.form["username"]) 
    
    return render_template("index.html")    

app.run(os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)
