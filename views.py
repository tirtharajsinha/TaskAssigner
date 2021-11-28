from flask import render_template, request, redirect
from models import Log
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
        id = log_add(person=person, task=task)
        print(id)
        return redirect("/submit?id="+str(id))

    print("create push")
    data = log_read()
    subd = Log.query.filter_by(submit='Submitted').all()
    dues = len(data)-len(subd)
    return render_template("create.html", data=data, total=len(data), subd=len(subd), dues=dues)


def upload():
    if request.method == 'POST':
        feed = str(request.form["feedback"])
        id = str(request.form["id"])
        if feed == "1":
            log_update(id=id)
            print("file uploaded for id "+id)
        return redirect("/")

    delr = request.args.get('del')
    print(delr)
    id = request.args.get('id')
    if(id == None):
        print("no id")
        return redirect("/")

    if delr != None:
        from app import db
        print("yes")
        Log.query.filter_by(id=id).delete()
        db.session.commit()

    data = log_read(filter=True, id=id)
    try:
        if data.submit == "Submitted":
            return redirect("/")
        task = data.task
        person = data.person
        return render_template("upload.html", task=task, person=person, id=id)
    except:
        return redirect("/")


def log_add(person="", task="", init=True):
    from app import db
    if init:
        today = date.today()
        today = today.strftime("%b-%d-%Y")
        data = Log(person=person, task=task, date=today, submit="Task Due")
        db.session.add(data)
        db.session.flush()
        db.session.refresh(data)
        print(data.id)
        db.session.commit()
        return data.id


def log_update(id, submit="Submitted"):
    from app import db
    data = Log.query.get(id)
    try:
        data.submit = submit
        db.session.add(data)
        db.session.commit()
    except:
        print("id not present")


def log_read(filter=False, id=0):
    from app import db
    if filter:
        return Log.query.get(id)
    all = Log.query.all()
    for data in all:
        print(data.id, data.person, data.task, data.date, data.submit)
    return all
