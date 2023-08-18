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
from ..models import default_sec

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

TITLES = ['View user', 'Edit user', 'New user']


def validate_assign_password(form):
    # if not form.errors:
    form.vars['password'] = default_sec
    print('form.vars', form.vars)


@action('users', method=['POST', 'GET'])
@action('users/<path:path>', method=['POST', 'GET'])
@action.uses('users.html', db, auth.user)
def index(path=None):
    print(db._lastsql)
    for r in db(db.auth_user.id > 0).select():
        print('xxxxxx', r['password'])
    # if path and path.split('/')[0] == 'edit':
    #     db.auth_user.password.value = default_sec
    #     print('action is edit', db.auth_user.password.value)

    query = (db.auth_user.id > 0)
    grid = Grid(path,
                formstyle=FormStyleBulma,  # FormStyleDefault or FormStyleBulma
                grid_class_style=GridClassStyleBulma,  # GridClassStyle or GridClassStyleBulma
                query=query,
                orderby=[db.auth_user.last_name],
                auto_process=False,
                validation=validate_assign_password,
                #  search_queries=[['Search by Name', lambda val: db.person.name.contains(val)]]
                )
    title = TITLES[0]
    attrs = {
        "_onclick": "window.history.back(); return false;",
        "_class": "button is-info is-outlined ml-2",
    }
    grid.param.new_sidecar = A("Back", **attrs)
    grid.param.edit_sidecar = A("Back", **attrs)

    # if path and path.split('/')[0] == 'edit':
    #     print('grid.form.validation = assign_password')
    #     # grid.validation = validate_assign_password
    #     grid.validation = validate_assign_password

    grid.process()

    if path:
        if path.split('/')[0] == 'details':
            e = grid.form.structure.find('.button')
            for el in e:
                if el['_value'] == 'Submit':
                    el['_value'] = 'Back'
                    el['_class'] = el['_class'] + ' is-info is-outlined'
        else:
            # attrs = {
            #     "_onclick": "window.history.back(); return false;",
            #     "_class": "button is-info is-outlined ml-2",
            # }
            # grid.param.new_sidecar = A("Back", **attrs)
            # grid.param.edit_sidecar = A("Back", **attrs)

            if path.split('/')[0] == 'edit':
                title = TITLES[1]
                grid.form.deletable = False
            else:
                title = TITLES[2]

    return dict(grid=grid, title=title)


@action('libraries', method=['POST', 'GET'])
@action('libraries/<path:path>', method=['POST', 'GET'])
@action.uses(db, auth.user)
def libraries(path=None):

    return dict()
