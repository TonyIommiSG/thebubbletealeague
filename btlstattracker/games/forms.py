#games/forms.py
from flask_wtf import FlaskForm,Form
from wtforms import StringField, PasswordField, SubmitField,DateField,SelectField,RadioField,FieldList,FormField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed
from btlstattracker import db

#from flask_login import current_user
from btlstattracker.models import User,Players,GamesFromRiot
from btlstattracker.games.matchinfofunctions import getTeamPlayers,getListOfPlayers,getChampList
from flask import session
from btlstattracker.games.views import session
import json

class MatchInfo(FlaskForm):

    api = StringField('Paste Your Riot API Here:',validators=[DataRequired()])
    match_id = StringField('Paste Match ID Here:',validators=[DataRequired()])
    season_number = StringField('Enter Season Number For Game:',validators=[DataRequired()])
    game_week = StringField('Enter Week Number For Game:',validators=[DataRequired()])
    #TODO: fix datefield, it is not popping up with proper info
    #game_date = DateField('Game Date',format='%Y/%m/%d',validators=[DataRequired()])
    submit = SubmitField('Click to submit for Match Info')


class TeamInfo(FlaskForm):

    blue_team = SelectField('Choose Blue Team', validators=[DataRequired()])
    red_team = SelectField('Choose Red Team', validators=[DataRequired()])
    submit = SubmitField('Click to submit for Match Info')

class PlayerInfo(FlaskForm):

    # position = SelectField(f'Choose {v[0]}\'s Champ: ', validators=[DataRequired()])
    # sub = SelectField('If position was subbed, choose from list: ')

    blue_top = SelectField('Choose Blue Top\'s Champ: ', validators=[DataRequired()])
    blue_top_sub = SelectField('If position was subbed, choose from list: ')
    blue_jungle = SelectField('Choose Blue Jungle\'s Champ: ', validators=[DataRequired()])
    blue_jungle_sub = SelectField('If position was subbed, choose from list: ')
    blue_middle = SelectField('Choose Blue Middle\'s Champ: ', validators=[DataRequired()])
    blue_middle_sub = SelectField('If position was subbed, choose from list: ')
    blue_adc = SelectField('Choose Blue ADC\'s Champ: ', validators=[DataRequired()])
    blue_adc_sub = SelectField('If position was subbed, choose from list: ')
    blue_support = SelectField('Choose Blue Support\'s Champ: ', validators=[DataRequired()])
    blue_support_sub = SelectField('If position was subbed, choose from list: ')

    red_top = SelectField('Choose Red Top\'s Champ: ', validators=[DataRequired()])
    red_top_sub = SelectField('If position was subbed, choose from list: ')
    red_jungle = SelectField('Choose Red Jungle\'s Champ: ', validators=[DataRequired()])
    red_jungle_sub = SelectField('If position was subbed, choose from list: ')
    red_middle = SelectField('Choose Red Middle\'s Champ: ', validators=[DataRequired()])
    red_middle_sub = SelectField('If position was subbed, choose from list: ')
    red_adc = SelectField('Choose Red ADC\'s Champ: ', validators=[DataRequired()])
    red_adc_sub = SelectField('If position was subbed, choose from list: ')
    red_support = SelectField('Choose Red Support\'s Champ: ', validators=[DataRequired()])
    red_support_sub = SelectField('If position was subbed, choose from list: ')

    submit = SubmitField('Click to submit for Match Info')
