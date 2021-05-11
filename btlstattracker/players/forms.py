#players/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField,RadioField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed

from flask_login import current_user
from btlstattracker.models import User

roles = [('Top','Top'),('Jungle','Jungle'),('Mid','Mid'),('ADC','ADC'),('Support','Support')]
sub_or_player_choice = [('Sub','Sub'),('Player','Player')]

class AddPlayer(FlaskForm):
    #roles = [('Top','Top'),('Jungle','Jungle'),('Mid','Mid'),('ADC','ADC'),('Support','Support')]
    #sub_or_player_choice = [('Sub','Sub'),('Player','Player')]

    summoner = StringField('Paste Summoner Name Here: ',validators=[DataRequired()])
    role = SelectField('Choose Role: ',choices = roles,validators=[DataRequired()])
    team = StringField('Type In Team Abbreviation: ',validators=[DataRequired()])
    sub_or_player = RadioField('Select whether player is a Sub or Player',choices=sub_or_player_choice,validators=[DataRequired()])
    submit = SubmitField('Click to add player to database')

    def check_summoner(self,field):
        if User.query.filter_by(summoner=field.data).first():
            raise ValidationError('This summoner has been added already!')

class SelectPlayer(FlaskForm):
    update_or_delete = [('update','Update'),('delete','Delete')]

    summoner = StringField('Paste Summoner Name Here: ',validators=[DataRequired()])
    update_or_delete_player = RadioField('Update or Delete this Player?',choices=update_or_delete,validators=[DataRequired()])
    submit = SubmitField('Click to confirm your choice.')

class UpdatePlayer(FlaskForm):

    summoner = StringField('Update Summoner Name Here: ')
    role = SelectField('Change Role: ',choices = roles)
    team = StringField('Update Team Abbreviation: ')
    sub_or_player = RadioField('Select whether player is a Sub or Player',choices=sub_or_player_choice,validators=[DataRequired()])
    submit = SubmitField('Click to submit changes to player')

    def check_summoner(self,field):
        if User.query.filter_by(summoner=field.data).first():
            raise ValidationError('This summoner already exists!')
