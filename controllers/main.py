"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from apps.scaffold_bulma_2.common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from apps.scaffold_bulma_2.models import get_user_email

from py4web.utils.grid import Grid, GridClassStyleBulma
from py4web.utils.form import FormStyleBulma
from yatl.helpers import *

url_signer = URLSigner(session)


@action('index')
@action.uses('index.html', db, auth)
def index():
    # print("User:", get_user_email())
    return dict()


# @action('users')
# @action.uses(db, auth, 'users.html')
# def users():
#     user_list = db(db.auth_user.id > 0).select()
#     return dict(user_list=user_list)


@action('users', method=['POST', 'GET'])
@action('users/<path:path>', method=['POST', 'GET'])
@action.uses('users.html', db, auth.user)
def index(path=None):
    query = (db.auth_user.id > 0)
    grid = Grid(path,
                formstyle=FormStyleBulma,  # FormStyleDefault or FormStyleBulma
                grid_class_style=GridClassStyleBulma,  # GridClassStyle or GridClassStyleBulma
                query=query,
                orderby=[db.auth_user.last_name],
                #  search_queries=[['Search by Name', lambda val: db.person.name.contains(val)]]
                )
    title = ''
    if path:
        if path.split('/')[0] == 'details':
            title = 'View user'
            e = grid.form.structure.find('.button')
            for el in e:
                if el['_value'] == 'Submit':
                    el['_value'] = 'Back'
                    el['_class'] = el['_class'] + ' is-info is-outlined'
        elif path.split('/')[0] == 'edit':
            title = 'Edit user'
            grid.form.deletable = False
            attrs = {
                "_onclick": "window.history.back(); return false;",
                "_class": "button is-info is-outlined ml-2",
            }
            grid.form.param.sidecar.append(A("Back", **attrs))
        else:
            title = 'New user'
    return dict(grid=grid, title=title)
