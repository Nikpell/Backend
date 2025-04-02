from sanic import Blueprint

from api.admin import admin
from api.login import login
from api.data import data
from api.payment import payment
from api.user import user

ap = Blueprint.group(login,
                     data,
                     admin,
                     user,
                     payment,
                     url_prefix="/api"
                      )