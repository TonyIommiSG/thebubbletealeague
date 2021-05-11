#models.py
from btlstattracker import db,app#,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore,Security
from datetime import datetime
import psycopg2


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(user_id)


roles_users = db.Table('roles_users',
                        db.Column('user_id',
                        db.Integer,
                        db.ForeignKey('user.id')),
                        db.Column('role_id',db.Integer,
                        db.ForeignKey('role.id')))

class User(db.Model,UserMixin):

    __tablename__ = 'user'

    id = db.Column(db.Integer,primary_key=True)
    profile_image = db.Column(db.String(64),nullable=False,default='default_profile.png')
    email = db.Column(db.String(255), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')
    # reset_password_token = db.Column(db.String(100), nullable=False, server_default='')
    active = db.Column(db.Boolean())
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    roles = db.relationship('Role',secondary='roles_users',
                            backref=db.backref('users') ,lazy='dynamic')

    def __init__(self,email,username,password,active,roles):
        self.email = email
        self.username = username
        self.password = password
        #self.password = generate_password_hash(password)
        self.active = active
        self.roles = roles

    def check_password(self,password):
        return check_password_hash(self.password,password)

    def __repr__(self):
        return f'Username {self.username}'

class Role(db.Model,RoleMixin):

    __tablename__ = 'role'

    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self,name):
        self.name = name

class Games(db.Model):

    __tablename__ = 'Games'

    id = db.Column(db.Integer,primary_key=True)
#TODO: update model to get rid of date column
    season = db.Column('Season',db.Integer,nullable=False)
    game_week = db.Column('Game Week',db.Integer,nullable=False)
    playoff_or_regular = db.Column('Playoff or Regular',db.String)
    summoner = db.Column('Summoner',db.String(16),nullable=False)
    role = db.Column('Role',db.String(8),nullable=False)
    team = db.Column('Team',db.String(8),nullable=False)
    sub_or_player = db.Column('Sub or Player',db.String(8),nullable=False)
    champion_id = db.Column('championId',db.String(16),nullable=False)
    game_duration = db.Column('gameDuration',db.Integer,nullable=False)
    game_id = db.Column('gameId',db.Integer,nullable=False)
    ban_1 = db.Column('ban 1',db.Integer)
    ban_2 = db.Column('ban 2',db.Integer)
    ban_3 = db.Column('ban 3',db.Integer)
    ban_4 = db.Column('ban 4',db.Integer)
    ban_5 = db.Column('ban 5',db.Integer)
    win = db.Column(db.String(8),nullable=False)
    kills = db.Column(db.Integer,nullable=False)
    deaths = db.Column(db.Integer,nullable=False)
    assists = db.Column(db.Integer,nullable=False)
    total_damage_dealt = db.Column('totalDamageDealt',db.Float,nullable=False)
    vision_score = db.Column('visionScore',db.Float,nullable=False)
    gold_earned = db.Column('goldEarned',db.Integer,nullable=False)
    total_minions_killed = db.Column('totalMinionsKilled',db.Integer,nullable=False)
    first_blood_kill = db.Column('firstBloodKill',db.String(8),nullable=False)
    creeps_per_min_deltas_0_10 = db.Column('creepsPerMinDeltas: 0-10',db.Float)
    creeps_per_min_deltas_10_20 = db.Column('creepsPerMinDeltas: 10-20',db.Float)
    creeps_per_min_deltas_20_30 = db.Column('creepsPerMinDeltas: 20-30',db.Float)
    creeps_per_min_deltas_30_end = db.Column('creepsPerMinDeltas: 30-end',db.Float)
    gold_per_min_deltas_0_10 = db.Column('goldPerMinDeltas: 0-10',db.Float)
    gold_per_min_deltas_10_20 = db.Column('goldPerMinDeltas: 10-20',db.Float)
    gold_per_min_deltas_20_30 = db.Column('goldPerMinDeltas: 20-30',db.Float)
    gold_per_min_deltas_30_end = db.Column('goldPerMinDeltas: 30-end',db.Float)

class Players(db.Model):

    __tablename__ = 'Players'

    id = db.Column(db.Integer,primary_key=True)
    summoner = db.Column('Summoner',db.String(16),unique=True,nullable=False)
    role = db.Column('Role',db.String(8),nullable=False)
    team = db.Column('Team',db.String(8),nullable=False)
    sub_or_player = db.Column('Sub or Player',db.String(8),nullable=False)

class GamesFromRiot(db.Model):

    __tablename__ = 'GamesFromRiot'

    #id = db.Column(db.Integer,primary_key=True)
    match_id = db.Column('gameId',db.Integer,nullable=False)
    game = db.Column(db.Text,primary_key=True)

#db.create_all()
#psycopg2.connect()
from btlstattracker.security.forms import ExtendedRegisterForm
user_datastore = SQLAlchemyUserDatastore(db,User, Role)
security = Security(app,user_datastore,register_form=ExtendedRegisterForm)
