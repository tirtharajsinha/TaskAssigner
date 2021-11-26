from flask import render_template, request, redirect
import os
from datetime import date
import warnings
warnings.filterwarnings("ignore")

# put your views here.


def index():
    if request.method == 'POST':
        return render_template("upload.html")

    return render_template("index.html")


def create():
    if request.method == 'POST':
        person = str(request.form["person"])
        task = str(request.form["task"])
        print(person, task)
        return redirect("/submit?person="+person+"&task="+task)

    print("create push")
    return render_template("create.html", total=0, subd=0, dues=0)


def upload():
    if request.method == 'POST':
        feed = str(request.form["feedback"])
        id = str(request.form["id"])
        if feed == "1":
            print("file uploaded for id "+id)
        return redirect("/")
    person = request.args.get('person')
    task = request.args.get('task')
    if(task == None):
        print("no id")
        return redirect("/")

    return render_template("upload.html", task=task, person=person, id="0")
