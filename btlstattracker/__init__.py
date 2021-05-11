# btlstattracker/__init__.py
from flask import Flask,session,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_admin import Admin, AdminIndexView
from flask_security import SQLAlchemyUserDatastore,Security,current_user
from flask_admin.contrib.sqla import ModelView


csrf_protect = CSRFProtect()
bcrypt = Bcrypt()
app = Flask(__name__)

class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self,name,**kwargs):
        return redirect(url_for('security.login',next=request.url))


class AdminView(AdminMixin,ModelView):
    pass

class HomeAdminView(AdminMixin,AdminIndexView):
    pass

admin = Admin(app, 'BTL Main Site', url='/', index_view=HomeAdminView(name='Home'))
app.config.from_object('btlstattracker.settings')
# Load environment specific settings
app.config.from_object('btlstattracker.local_settings')
csrf_protect.init_app(app)
bcrypt.init_app(app)

# #####################################
# ### DATABASE SETUP ##############
# ##########################

db = SQLAlchemy(app)
Migrate(app,db)


# #######################
# ### LOGIN CONFIGS
# login_manager = LoginManager()
#
# login_manager.init_app(app)
# login_manager.login_view = 'user.login'


#######################################################

from btlstattracker.core.views import core
from btlstattracker.error_pages.handlers import error_pages
#from btlstattracker.user.views import user
from btlstattracker.games.views import games
from btlstattracker.players.views import players
from btlstattracker.models import *


app.register_blueprint(core)
app.register_blueprint(error_pages)
#app.register_blueprint(user)
app.register_blueprint(games)
app.register_blueprint(players)

admin.add_view(AdminView(User, db.session,endpoint='model_user'))
admin.add_view(AdminView(Games, db.session,endpoint='model_games'))
admin.add_view(AdminView(GamesFromRiot, db.session))
admin.add_view(AdminView(Players, db.session,endpoint='model_players'))
