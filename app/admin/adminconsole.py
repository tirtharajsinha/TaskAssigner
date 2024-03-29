from models import db, User, admin_history, Log
from flask_admin import Admin, BaseView, expose, Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import Flask, redirect, render_template, Markup
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, current_user
from datetime import datetime
import urls

############################################
# DOCS
# Register model here to see your model in admin page.
# first import your Model
# go to add_adminview function at the end of the file.
# follow the other model register mothod.
# register your model before return statement.
############################################


def load_history(model, event):
    # print(model.id, model.__tablename__)
    # print("-" * 10)
    # return
    now = datetime.now()
    newhist = admin_history(
        username=current_user.username,
        table=model.__tablename__,
        event=event,
        row_id=model.id,
        time=now.strftime("%d/%m/%Y %H:%M:%S"),
    )

    db.session.add(newhist)
    db.session.commit()


def read_history():
    return admin_history.query.order_by(admin_history.id.desc())


class AdminView(AdminIndexView):
    @expose("/")
    def index(self):
        history = read_history()
        return self.render("admin/admin_base.html", user=current_user, history=history)

    def is_accessible(self):
        perm = (
            current_user.is_authenticated
            and current_user.permission == "admin"
            and current_user.is_active
        )
        return perm

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect("/login?next=/admin")


class DBModelView(ModelView):
    create_template = "admin/microblog_create.html"
    edit_template = "admin/microblog_edit.html"

    def is_accessible(self):
        perm = (
            current_user.is_authenticated
            and current_user.permission == "admin"
            and current_user.is_active
        )
        return perm

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect("/login")

    def after_model_change(self, form, model, is_created):
        print(model.__tablename__, model.id, is_created, "----------------->")
        event = "edited"
        if is_created:
            event = "created"
        load_history(model, event)

    def after_model_delete(self, model):
        event = "deleted"
        print(model.__tablename__, model.id, "----------------->")
        load_history(model, event)

    def _description_formatter(view, context, model, name):
        return model.desc[:30]

    def _image_formatter(view, context, model, name):
        return model.image[:30]

    def _icon_formatter(view, context, model, name):
        return model.icon[:30]

    def _assignee_formatter(view, context, model, name):
        return Markup(f"<a href='/static/media/{model.assignee}'>{model.assignee}</a>")

    column_formatters = {
        "desc": _description_formatter,
        "image": _image_formatter,
        "icon": _icon_formatter,
        "assignee": _assignee_formatter,
    }


class AdminModelView(ModelView):
    create_template = "admin/microblog_create.html"
    edit_template = "admin/microblog_edit.html"
    can_export = True

    def is_accessible(self):
        perm = (
            current_user.is_authenticated
            and current_user.permission == "admin"
            and current_user.is_active
        )
        return perm

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect("/login")


# setting up admin panel
def get_admin(app):
    admin = Admin(
        app,
        name="admin panel",
        index_view=AdminView(
            name="Home",
            menu_icon_type="glyph",
            menu_icon_value="glyphicon-home",
            url="/admin",
        ),
    )
    admin = add_adminview(admin)
    admin.add_view(AdminModelView(admin_history, db.session))

    return admin


def add_adminview(admin):
    admin.add_view(DBModelView(User, db.session))
    admin.add_view(DBModelView(Log, db.session))
    return admin
