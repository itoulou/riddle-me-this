import os
import json
import operator
from itertools import groupby
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

riddle_index = 0
counter = 0
final_score = 0
current_user = ""


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
    """
    function which returns all user
    """
    users = []
    
    with open("data/user_played.txt", "r") as user_played:
        users = user_played.readlines()
    return users    
        
def get_all_scores():
    """
    function that returns all scores
    """
    scores = []
    
    with open("data/score.txt", "r") as user_score:
        scores = user_score.readlines()
    return map(int, scores)
    #map(int, scores) to change the score value from string to an int

@app.route('/', methods=["GET", "POST"])
def index():
    global current_user
    """
    send username to usernames.txt file and send to user's homepage
    """
    if request.method == "POST":
        write_to_file("data/usernames.txt", request.form["username"] + "\n")
        current_user = request.form["username"]
        return redirect(request.form["username"]) 
    
    return render_template("index.html")    

@app.route('/<username>', methods = ["GET", "POST"])
def user(username):
    """
    displays riddles and handles answers. Score and riddle_index
    is incremented by 1 if answer is correct. User can move to next question.
    """
    global riddle_index, counter, final_score
    data = []
    with open("data/riddles.json", "r") as json_data:
        data = json.load(json_data)
      
    if request.method == "POST" and "check" in request.form:
        #Click check button to see if answer is correct
        if request.form["answer"].lower().strip() == data[riddle_index]["answer"]:
            if riddle_index >= counter:
                """
                to prevent score increasing if check button pressed multiple
                times on same question
                """
                counter += 1
                riddle_index += 1
                 
                if len(data) == riddle_index:
                    #move to exitgame.html page if game is finished
                    #save username to user_played.txt for leaderboard
                    #save score to score.txt
                    riddle_index = 0
                    save_user(username, "user_played")
                    save_score(counter)
                    final_score = counter
                    counter = 0
                    return redirect(url_for('show_exitgame'))
            
                return render_template("riddles.html", username = username, data = data[riddle_index]["question"])
                
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
            final_score = counter
            counter = 0
            return redirect(url_for('show_exitgame'))
                
        return render_template("riddles.html", username = username, data = data[riddle_index]["question"])
    
    elif request.method == "POST" and "previous" in request.form:
        if riddle_index >= 1:
            #to previous riddle
            riddle_index -= 1
            if len(data) < 0:
                riddle_index = 0
            return render_template("riddles.html", username = username, data = data[riddle_index]["question"])
        else:
            riddle_index = 0
            return render_template("riddles.html", username = username, data = data[riddle_index]["question"])

    if request.method == "POST" and "exit-game" in request.form:
        return redirect("/") 
    
    if request.method == "POST" and "leaderboard" in request.form:
        return redirect('/leaderboard')             
    
    return render_template("riddles.html", username = username, data = data[riddle_index]["question"])
    
@app.route('/exitgame', methods = ["GET", "POST"])
def show_exitgame():
    """
    shows score of the user where user can replay, exit game or
    look at the leaderboard
    """
    if request.method == "POST" and "play-again" in request.form:
        return redirect('/{0}'.format(current_user))

    if request.method == "POST" and "exit-game" in request.form:
        return redirect("/") 
    
    if request.method == "POST" and "leaderboard" in request.form:
        return redirect('/leaderboard') 
        
    return render_template("exitgame.html", mark = final_score)    
    

@app.route('/leaderboard', methods = ["GET", "POST"])
def show_leaderboard():
    """
    adds user and their score to leaderboard
    if score is within the 7th highest
    """
    if request.method == "POST" and "return" in request.form:
        return redirect("/exitgame")
    
    scores = get_all_scores()
    
    users = get_all_users_played()
    
    leaderboard = zip(users, scores)
    trimmed_leaderboard = []
    
    for item in leaderboard:
        trimmed_leaderboard.append((item[0].strip("\n"), item[1]))
    
    sorted_leaderboard_by_score = sorted(trimmed_leaderboard, key = operator.itemgetter(1), reverse=True) 
    
    row_counter = 0
    FULL_HTML = [] #create an array to show final table where every username
                   #and score is put into
                   
    for username, rows in groupby(sorted_leaderboard_by_score, operator.itemgetter(0)):
        table = []
        
        for username, score in rows:
            table.append("<tr><td>{0}</td><td>{1}</td></tr>".format(username, score))
            row_counter += 1
            if row_counter == 7:
                break
        table = "\n{0}\n".format("\n".join(table))   
        FULL_HTML.append(table)
        
        if row_counter == 7:
            break
        # append every row to FULL_HTML
    
    return render_template("leaderboard.html", table = "".join(FULL_HTML))
    # join a new row for every ""
  
app.run(os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)
