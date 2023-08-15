from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SECRET_KEY"] = "my secret key"

#Initialize the db

db = SQLAlchemy(app)
with app.app_context():
    db.create_all()
# Define model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(200), nullable = False, unique = True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    #Create A string
    def __repr__(self):
        return "<Name %r>" % self.name

#Create Form Class
class NamerForm(FlaskForm):
    name = StringField("What your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")

#Create Form Class
class UserForm(FlaskForm):
    name = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route("/")
def index():

    favorite=["Peperoni", "cheese", "tomatoes", 50]
    return render_template("index.html", favorite = favorite)

@app.route("/user/<name>")
def user(name):
    return render_template("users.html", user_name=name)


@app.route("/name", methods=["GET", "POST"])
def name():
    name = None
    form = NamerForm()
    #Validate Form submitions
    if form.validate_on_submit():
        name = form.name.data
        #clear it for the next time
        form.name.data = ""
        flash("Form Submitted successfully")

    return render_template("name.html", name=name, form=form)

# Add new user
@app.route("/user/add", methods=["GET", "POST"])
def add_user():
    name = None
    form = UserForm()
    #Validate Form submitions
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name = form.name.data, email = form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        #clear it for the next time
        form.name.data = ""
        form.email.data = ""
        flash("User added successfully")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form=form, name=name, our_users = our_users)


# Update user from database
@app.route("/update/<int:id>", methods = ["GET", "POST"])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)

    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        try:
            db.session.commit()
            flash("User updated successfully!")
            return render_template("update_user.html", form=form, name_to_update = name_to_update)
        except:
            flash("Error! There was a problem!")
            return render_template("update_user.html", form=form, name_to_update = name_to_update)
    else:
        return render_template("update_user.html", form=form, name_to_update = name_to_update, id=id)

# Update user from database
@app.route("/delete/<int:id>", methods = ["GET", "POST"])
def delete(id):
    form = UserForm()
    name = None
    name_to_delete = Users.query.get_or_404(id)

    try:
        db.session.delete(name_to_delete)
        db.session.commit()
        flash("User deleted successfully!")
        return render_template("add_user.html", form=form, name_to_delete = name_to_delete, id=id)
    except:
        flash("Error! There was a problem!")
        return render_template("add_user.html", form=form, name_to_update = name_to_delete, id=id)



#Create Custom Error Pages
#Ivalid URL
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

#Internal server error
@app.errorhandler(500)
def page_not_found(error):
    return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(debug=True)