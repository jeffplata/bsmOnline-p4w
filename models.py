"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *

key = ''
DEFAULT_SEC = 'Password1'
default_sec = str(CRYPT(key="pbkdf2(1000,20,sha512):%s" % key)(DEFAULT_SEC)[0])


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()


db.define_table(
    'region',
    Field('region_name'),
    Field('region_shortname'),
    auth.signature,
    )



### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later


db.commit()
