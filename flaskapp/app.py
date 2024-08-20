from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    time = db.Column(db.DateTime, default=datetime.now)

@app.route("/", methods=["GET", "POST"])
def flask_app():
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        new_todo = Todo(title=title, desc=desc)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("flask_app"))
    alltodo = Todo.query.all()
    return render_template("index.html", alltodo=alltodo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(Sno=sno).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for("flask_app"))
 
@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    todo = Todo.query.filter_by(Sno=sno).first()
    if request.method == "POST":
        todo.title = request.form["title"]
        todo.desc = request.form["desc"]
        db.session.commit()
        return redirect(url_for("flask_app"))
    return render_template("update.html", todo=todo)

@app.route("/lists")
def lists():
    search_query = request.args.get('search')
    if search_query:
        alltodo = Todo.query.filter(Todo.title.contains(search_query)).all()
    else:
        alltodo = Todo.query.all()
    return render_template("lists.html", alltodo=alltodo)
    

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
