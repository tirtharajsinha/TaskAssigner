from admin import auth


# config your urls here
def add_url(app):
    import views

    app.add_url_rule("/", view_func=views.index, methods=["GET", "POST"])
    # app.add_url_rule("/adminlogin", view_func=auth.adminlogin, methods=["GET", "POST"])
    app.add_url_rule("/login", view_func=auth.adminlogin, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=auth.logout, methods=["GET", "POST"])

    app.add_url_rule("/tasks", view_func=views.tasks, methods=["GET", "POST"])
    app.add_url_rule(
        "/sendmail/<id>", view_func=views.send_email, methods=["GET", "POST"]
    )
    app.add_url_rule(
        "/getassignee/<id>", view_func=views.read_assignee, methods=["GET", "POST"]
    )
    return app
