import os
import json
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

riddle_index = 0
counter = 0

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
    send username to usernames.txt file and send to user's homepage
    """
    if request.method == "POST":
        write_to_file("data/usernames.txt", request.form["username"] + "\n")
        
        return redirect(request.form["username"]) 
    
    return render_template("index.html")    

@app.route('/<username>', methods = ["GET", "POST"])
def user(username):
    global riddle_index, counter
    data = []
    
    with open("data/riddles.json", "r") as json_data:
        data = json.load(json_data)
        
      
    if request.method == "POST" and "check" in request.form:
        #Click check button to see if answer is correct
        if request.form["answer"].lower() == data[riddle_index]["answer"]:
            
            counter += 1
            return render_template("riddles.html", username = username, data = data[riddle_index]["question"], correct = "Correct!")
            
        else:
           #if answer is incorrect 
            return render_template("riddles.html", username = username, data = data[riddle_index]["question"], correct = "Wrong answer, try again")
            
    elif request.method == "POST" and "next" in request.form:
        #to next riddle
        
        riddle_index += 1
        
        if len(data) == riddle_index:
            #move to new a page if game is finished
            riddle_index = 0
            return render_template("exitgame.html", mark = counter)
            
            
                
        return render_template("riddles.html", username = username, data = data[riddle_index]["question"])
    
    elif request.method == "POST" and "previous" in request.form:
        #to previous riddle
        riddle_index -= 1
        if len(data) < 0:
            riddle_index = 0
        return render_template("riddles.html", username = username, data = data[riddle_index]["question"])

    if request.method == "POST" and "exit-game" in request.form:
                return render_template("index.html") 
    
    if request.method == "POST" and "leaderboard" in request.form:
                return redirect(/'leaderboard')             
    
    return render_template("riddles.html", username = username, data = data[riddle_index]["question"])
    
    
@app.route('/leaderboard', methods = ["GET"])
def show_leaderboard():
    

  
app.run(os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)
