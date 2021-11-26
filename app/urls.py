import views

# config your urls here


def add_url(app):
    app.add_url_rule('/', view_func=views.create, methods=['GET', 'POST'])
    app.add_url_rule('/create', view_func=views.create,
                     methods=['GET', 'POST'])
    app.add_url_rule('/submit', view_func=views.upload,
                     methods=['GET', 'POST'])

    return app
