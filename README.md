# <a href="https://riddle-me-this-tou.herokuapp.com/" target="_blank">Riddle me this</a>

The brief for this assignment was to produce a web application riddle based game
where users ask a series of riddles.

This web application is an insight to testing my python skills by creating a
riddles game. Learning how to write and read from files has allowed me to manipulate data
submitted by the user and respond to their answers and save scores providing a 
fun game that users want to play more than once. 

# UX
This game is great for any quiz enthusiast or ones who enjoy a good puzzle.
It can be used in schools for younger children or adults who want test their
riddles skills.

I wanted to provide users with a fun and enjoyable game where users would want to
play more than once. In order to achieve this I created a leaderboard where the user can
beat other users, their friends or their own score.
I believe a user would be more likely to play a game that is aesthetically pleasing
so this web application has an easy-on-the-eye and simple colour scheme. It is
also responsive on several screen widths and browsers to make sure anybody can
play anywhere.

### Riddles
__md/lg__

![riddles image](/wireframes/images/riddles-md-lg.png "riddles md lg")

__xs/sm__

![riddles image](/wireframes/images/riddles-xs-sm.png "riddles xs sm")


# Features
### Homepage
* __Enter username__
    * Users can enter a username which will be displayed on the riddles page and leaderboard
    and click 'Play' button to initiate the game.

### Riddles
* __Check__
    * Users can check their answer given by clicking 'Check' button. If answer is correct
    they move onto next riddle.

* __Previous__
    * User can move to previous riddle by clicking 'Previous' button if the question
    number isn't zero

* __Next__
    * User can move to next riddle by clicking 'Next' button.

### Exitgame
* __Exit__
    *  User can exit or replay game by clicking 'Exit'.

* __Leaderboard__
    *  User can see leaderboard by clicking 'Leaderboard' button. 

### Leaderboard
* If user's score is within the top 7 scores then their username and score
will be displayed on the leaderboard in order of score.

# Technologies used
* [__HTML__](https://devdocs.io/html/) 
    * This project uses HTML to provide the content.
* [__CSS__](https://devdocs.io/css/) 
    * This project uses CSS to provide the styles.
* [__Bootstrap__](https://getbootstrap.com/docs/3.3/getting-started/)
    * This project uses Bootstrap framework to simplify grid layout and provide a better UX. 
* [__Python__](https://docs.python.org/release/3.4.3/)
    * This project uses Python to handle POSTs and manipulate data presented from the user.
* [__Flask__](http://flask.pocoo.org/docs/1.0/)
    * This project uses Flask to create URLs easily and use a tool to simplify the creation of this web application . 


# Testing
### Index
1. Try to submit the empty form and verify that an error message about the required fields appears.
2. Try to submit the form with all inputs valid and verify you are redirected to the 'riddles' page.

### Check
1. Click the 'CHECK' button.
2. Try to submit the empty form and verify that an error message appears.
3. Try to submit the form with incorrect answer and verify an error message appears stating the answer is wrong.
4. Try to submit the form with a valid input and verify you are redirected to the next riddle.

### Next
1. Click on the 'Next' button.
2. Verify that you are redirected to the next riddle without the user score increasing.
3. If riddle number equals 15 and 'Next' button clicked, verify that user is redirected to 'exitgame' page.

### Previous
1. Click on the 'Previous' button.
2. Verify that you are redirected to the previous riddle without the user score decreasing.
3. If riddle number equals 1 and 'Previous' button clicked, verify that user is redirected to first riddle and error message appears.

### Leaderboard
1. Click the 'Leaderboard' button on the 'exitgame' page.
2. Verify that user is redirected to 'Leaderboard' page.
3. Verify that user's score and username will be added to a row in leaderboard table.
4. If there are more than 7 scores on the table and user score is within
top 7 scores, verify that username and score will be added to leaderboard sorted by score.
5. Else user will not be added to the leaderboard

# Deployment
I have deployed this project to the hosting platform [__Heroku__](https://devcenter.heroku.com/categories/reference)
with a separate [__GitHub__](https://github.com/) branch.
### Config Vars
* IP
* PORT

# Credits
### Acknowledgments
* A big thank you to Victor Miclovich my mentor who's been extremely helpful with
the completion of this project.
* Another big thank you to all the Tutors at Code Institute for coping with my multitude of questions on a daily basis.