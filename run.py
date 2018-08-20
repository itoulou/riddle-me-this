import os
import json
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

riddle_index = 0

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
    
def add_answers(username, message):
    """
    Add messages to the `messages` list
    """
    write_to_file("data/users_answer.txt", "({0} - {1}\n".format(
           username.title(),
           message))
    
def get_all_answers():
    """
    Get all the messages and separate them by a `br`
    """
    messages = []
    with open("data/users_answer.txt", "r") as chat_messages:
        messages = chat_messages.readlines()
    return messages     

@app.route('/', methods=["GET", "POST"])
def index():
    """
    Handle POST
    """
    if request.method == "POST":
        write_to_file("data/usernames.txt", request.form["username"] + "\n")
        
        return redirect(request.form["username"]) 
    
    return render_template("index.html")    

@app.route('/<username>', methods = ["GET", "POST"])
def user(username):
    global riddle_index
    data = []
    
    with open("data/riddles.json", "r") as json_data:
        data = json.load(json_data)
        
      
    if request.method == "POST" and "check" in request.form:
        #Correct answer 
        if request.form["answer"].lower() == data[riddle_index]["answer"]:
            
            
            return render_template("riddles.html", username = username, data = data[riddle_index]["question"], correct = "Correct!")
            
        else:
            
            return render_template("riddles.html", username = username, data = data[riddle_index]["question"], correct = "Wrong answer, try again")
            
    elif request.method == "POST" and "next" in request.form:
        riddle_index += 1
        #if len(data) == riddle_index:
            #move to new a page
        
        return render_template("riddles.html", username = username, data = data[riddle_index]["question"])
    
    elif request.method == "POST" and "previous" in request.form:
        riddle_index -= 1
        if len(data) < 0:
            riddle_index = 0
        return render_template("riddles.html", username = username, data = data[riddle_index]["question"])

    
    
    return render_template("riddles.html", username = username, data = data[riddle_index]["question"])
    
    
    


  
app.run(os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)
