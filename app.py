from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Information(db.Model):
    __tablename__ = 'information'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String())
    surname = db.Column(db.String())
    dob = db.Column(db.String())
    phone = db.Column(db.String())
    address=db.Column(db.String())
    timezone=db.Column(db.String())

@app.route("/", methods=['GET', 'POST'])
def welcome():
    if request.method == "GET":
        return render_template("home.html")
    if request.method == "POST":
        user_id = request.form['content']
        return redirect('/user/{}'.format(user_id))

@app.route("/user/<int:id>", methods=['GET', 'POST'])
def operate(id):
    user = Information.query.get_or_404(id)

    if request.method == "GET":
        if user:
            return render_template("index.html", user=user)
        else:
            return render_template("not-found.html")

    if request.method == "POST":
        user.address = request.form['content']

        try:
            db.session.commit()
            return redirect('/user/{}'.format(id))

        except:
            return "There was an issue updating"
        return "Hello"


if __name__ == '__main__':
    app.run(debug=True)