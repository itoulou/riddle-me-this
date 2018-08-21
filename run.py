import os
import json
import operator
from itertools import groupby
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

riddle_index = 0
counter = 0


def write_to_file(filename, data):
    """
    Handle the process of writing data to a file
    """
    with open(filename, "a") as file:
        file.writelines(data)

def save_user(username, filename):
    """
    Add usernames to the `usernames.txt` list
    """
    write_to_file("data/{0}.txt".format(filename), "{0}\n".format(username))

def save_score(counter):
    """
    Save score of indivdual user to leaderboard.json JSON file
    """
    write_to_file("data/score.txt", "{0}\n".format(counter))

def get_all_users_played():
    
    users = []
    
    with open("data/user_played.txt", "r") as user_played:
        users = user_played.readlines()
    return users    
        
def get_all_scores():
    
    scores = []
    
    with open("data/score.txt", "r") as user_score:
        scores = user_score.readlines()
    return scores    

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
            if riddle_index >= counter:
                counter += 1
            
                return render_template("riddles.html", username = username, data = data[riddle_index]["question"], correct = "Correct!")
            else:
                return render_template("riddles.html", username = username, data = data[riddle_index]["question"], correct = "You've already answered this question correctly")

            
        else:
           #if answer is incorrect 
            return render_template("riddles.html", username = username, data = data[riddle_index]["question"], correct = "Wrong answer, try again")
            
    elif request.method == "POST" and "next" in request.form:
        #to next riddle
        
        riddle_index += 1
        
        if len(data) == riddle_index:
            #move to exitgame.html page if game is finished
            #save username to user_played.txt for leaderboard
            #save score to score.txt
            riddle_index = 0
            save_user(username, "user_played")
            save_score(counter)
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
                return redirect('/leaderboard')             
    
    return render_template("riddles.html", username = username, data = data[riddle_index]["question"])
    
   
@app.route('/leaderboard', methods = ["GET"])
def show_leaderboard():
    
    
    scores = get_all_scores()
    
    users = get_all_users_played()
    
    leaderboard = zip(users, scores)
    trimmed_leaderboard = []
    
    for item in leaderboard:
        trimmed_leaderboard.append((item[0].strip("\n"), item[1].strip("\n")))
    
    sorted_leaderboard_by_score = sorted(trimmed_leaderboard, key = operator.itemgetter(1), reverse=True) 
    
    row_counter = 0
    for username, rows in groupby(sorted_leaderboard_by_score, operator.itemgetter(0)):
        table = []
        for username, score in rows:
            table.append("<tr><td>{0}</td><td>{1}</td></tr>".format(username, score))
            row_counter += 1
            if row_counter == 2:
                break
        
        table = "\n{0}\n".format("\n".join(table))    
   
    return render_template("leaderboard.html", table = table)
      
    
  
app.run(os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)
