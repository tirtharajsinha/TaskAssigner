from flask import render_template, request, redirect, jsonify
from flask_login import current_user, login_required
from models import Log, db
import os
from datetime import date
from datetime import datetime
import warnings
import pandas as pd

# from app import db

from flask_mail import Mail, Message

warnings.filterwarnings("ignore")

# put your views here.


def index():
    if request.method == "POST":
        return "got a post request"

    return render_template("index.html", user=current_user)


def tasks():
    if current_user.is_anonymous:
        print("Not logged in")
        return redirect("/login")

    if request.method == "POST":
        Assignee = request.files["person"]
        task = str(request.form["task"])
        dept = str(request.form["dept"])
        duedate = request.form["duedate"]
        # print(person, task)
        id = log_add(Assignee=Assignee, task=task, duedate=duedate, dept=dept)
        print(id)
        if id != -1:
            mail_sender(id)
        # return redirect("/submit?id=" + str(id))

    print("create push")
    data = log_read()
    # subd = Log.query.filter_by(submit="Submitted").all()
    # dues = len(data) - len(subd)

    return render_template(
        "create.html", data=data, total=len(data), subd=0, dues=0, user=current_user
    )


def log_add(Assignee, task, duedate, dept, init=True):
    # from app import db

    if init:
        today = datetime.now()

        duedate = datetime.strptime(duedate, "%Y-%m-%dT%H:%M")

        uploads_dir = os.path.join(os.getcwd(), "static/media")
        try:
            os.makedirs(uploads_dir)
            print("Directory Created")
        except:
            print("Directory Exists")
        Assignee.save(os.path.join(uploads_dir, Assignee.filename))

        if extract_csv(Assignee.filename):
            print("Successfully parsed uploded file")
            data = Log(
                Assigner=current_user.username,
                assignee=Assignee.filename,
                task=task,
                date=today,
                DueDate=duedate,
                department=dept,
            )
            print(data)
            db.session.add(data)
            db.session.flush()
            db.session.refresh(data)
            print(data.id)
            db.session.commit()
            return data.id
        else:
            print("Could not parse uploaded file")
            return -1


def extract_csv(filename):
    uploads_dir = os.path.join(os.getcwd(), "static/media")

    try:
        print(filename.lower())
        if ".csv" in filename.lower():
            df = pd.read_csv(os.path.join(uploads_dir, filename))
            print("csv file found")
        elif ".xlsx" in filename.lower():
            df = pd.read_excel(os.path.join(uploads_dir, filename))
            print("Excel File Found")
        for ind in df.index:
            print(df["name"][ind], df["email"][ind])
        return True
    except Exception as e:
        print(e)
        return False


def log_read(filter=False, id=0):
    from app import db

    if filter:
        return Log.query.get(id)
    all = Log.query.order_by(Log.id.desc()).all()

    return all


def send_email(id):
    mail_sender(id)
    data = {"status": "OK"}
    return jsonify(data)


def mail_sender(id):
    from app import mail

    task = Log.query.get(id)
    if task == None:
        return
    uploads_dir = os.path.join(os.getcwd(), "static/media")

    if ".csv" in task.assignee.lower():
        df = pd.read_csv(os.path.join(uploads_dir, task.assignee))
    elif ".xlsx" in task.assignee.lower():
        df = pd.read_excel(os.path.join(uploads_dir, task.assignee))

    for ind in df.index:
        print(df["name"][ind], df["email"][ind])
        msg = Message(
            "Gentle Reminder -Task Due",
            sender="debayan462@gmail.com",
            recipients=[df["email"][ind]],
        )
        msg.body = f"""
        Hi,{df["name"][ind]},
        It's a gentle reminder that you have a task named {task.task} due on {task.DueDate.strftime('%d %b, %Y %I:%M %p')}
        You have assignments to be submitted. Please check the portal for further details
        
        
        Ignore if already submitted.
        from,
        IIM Lucknow, Department of {task.department}
        """

        mail.send(msg)


def read_assignee(id):
    task = Log.query.get(id)
    if task == None:
        return
    uploads_dir = os.path.join(os.getcwd(), "static/media")

    if ".csv" in task.assignee.lower():
        df = pd.read_csv(os.path.join(uploads_dir, task.assignee))
    elif ".xlsx" in task.assignee.lower():
        df = pd.read_excel(os.path.join(uploads_dir, task.assignee))

    assigneeList = []

    for ind in df.index:
        assigneeList.append({"name": df["name"][ind], "email": df["email"][ind]})

    data = {"filename": task.assignee, "list": assigneeList}
    return jsonify(data)
