import ombott as bottle

from py4web.core import Fixture
from .common import auth, db, Field
from pydal.validators import IS_NOT_EMPTY, IS_IN_DB, IS_NOT_IN_DB
from .models import USER_ADAM, DEFAULT_SEC


class requires_permission(Fixture):
    def __init__(self, permission_name, table_name):
        self.permission_name = permission_name
        self.table_name = table_name

    def on_request(self):
        if not has_permission(self.permission_name, self.table_name):
            bottle.abort(code=401, text='You do not have authorization to run this function.  Please contact support.')


def has_permission(permission_name, table_name):
    left = db.auth_permission.on(db.auth_membership.auth_group == db.auth_permission.auth_group)
    x = db((db.auth_membership.auth_user == auth.user_id) &
           (db.auth_permission.table_name == table_name) &
           (db.auth_permission.name == permission_name)).select(left=left)

    if len(x) == 0:
        return False
    else:
        return True


class requires_membership(Fixture):
    def __init__(self, role):
        self.role = role

    def on_request(self):
        if not has_membership(self.role):
            bottle.abort(code=401, text='You do not have authorization to run this function.  Please contact support.')


def has_membership(role):
    left = db.auth_permission.on(db.auth_membership.auth_group == db.auth_group.id)
    x = db((db.auth_membership.auth_user == auth.user_id) &
           (db.auth_group.role == role)).select(left=left)

    if len(x) == 0:
        return False
    else:
        return True


db.define_table('auth_group',
                Field('group_name', required=True,
                      requires=IS_NOT_EMPTY()))
db.auth_group.group_name.requires = IS_NOT_IN_DB(db, 'auth_group.group_name')


db.define_table('auth_membership',
                Field('auth_user', 'reference auth_user',
                      rname='user_id'),
                Field('auth_group', 'reference auth_group',
                      rname='group_id'))


db.define_table('auth_permission',
                Field('auth_group', 'reference auth_group',
                      rname='group_id',
                      requires=IS_IN_DB(db, 'auth_group.id',
                                        '%(role)s',
                                        zero='..')),
                Field('name', required=True,
                      requires=IS_NOT_EMPTY()),
                Field('table_name', required=True,
                      requires=IS_NOT_EMPTY()),
                Field('record', 'integer',
                      rname='record_id'))


# ==================

if db(db.auth_user.id).count() < 1:
    ret = db.auth_group.validate_and_insert(group_name='admin')
    group_id = ret.get('id')
    db.auth_permission.validate_and_insert(auth_group=group_id,name='manage',table_name='auth_user',record=0)
    ret = db.auth_user.validate_and_insert(email=USER_ADAM, first_name="admin", last_name="admin", password=DEFAULT_SEC)
    user_id = ret.get('id')
    db.auth_membership.validate_and_insert(auth_user=user_id, auth_group=group_id)
    db.commit()