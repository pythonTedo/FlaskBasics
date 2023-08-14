from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():

    favorite=["Peperoni", "cheese", "tomatoes", 50]
    return render_template("index.html", favorite = favorite)

@app.route("/user/<name>")
def user(name):
    return render_template("users.html", user_name=name)

#Create Custom Error Pages
#Ivalid URL
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

#Internal server error
@app.errorhandler(500)
def page_not_found(error):
    return render_template("500.html"), 500