#players/views.py
from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_user import current_user, login_required, roles_required
#TODO: add logout and login?
from btlstattracker import db
from btlstattracker.models import Players
from btlstattracker.players.forms import AddPlayer,SelectPlayer,UpdatePlayer
import sqlite3 as sql
import pandas as pd

players = Blueprint('players',__name__)

@players.route('/allplayers',methods=['GET'])
@login_required
@roles_required('admin')
def allplayers():
    df = pd.read_sql(sql = 'SELECT * FROM Players',con = db.session.bind,index_col =['id'] ,columns = ['Summoner','Role','Team','Sub or Player'])
    return render_template('allplayers.html',data=df.to_html())

#add player
@players.route('/addplayer',methods=['GET','POST'])
@login_required
@roles_required('admin')
def newplayer():
    form = AddPlayer()

    if form.validate_on_submit():
        player = Players(summoner=form.summoner.data,
                        role = form.role.data,
                        team = form.team.data,
                        sub_or_player = form.sub_or_player.data)
        db.session.add(player)
        db.session.commit()
        flash('Player added successfully!')
        return redirect(url_for('players.newplayer'))

    return render_template('addplayer.html',form=form)

#update player
@players.route('/update_or_delete_player',methods=['GET','POST'])
@login_required
@roles_required('admin')
def update_or_delete_player():
    form1 = SelectPlayer()

    if form1.validate_on_submit():

        summoner_choice = form1.summoner.data
        summoner_to_update = Players.query.filter_by(summoner=summoner_choice).first()

        if form1.update_or_delete_player.data == 'update':

            form2 = UpdatePlayer()

            if form2.validate_on_submit():
                summoner_to_update.summoner = form2.summoner.data
                summoner_to_update.role = form2.role.data
                summoner_to_update.team = form2.team.data
                summoner_to_update.sub_or_player = form2.sub_or_player.data
                db.session.commit()
                flash('Player Updated')
                return redirect(url_for('players.update_or_delete_player'))
            return render_template('updateplayer.html',form2=form2)

        elif form1.update_or_delete_player.data == 'delete':

            if form1.validate_on_submit():
                db.session.delete(summoner_to_update)
                db.session.commit()
                flash('Player has been deleted')
                return redirect(url_for('core.index'))
            return render_template('update_or_delete_player.html',form1=form1)
    return render_template('update_or_delete_player.html',form1=form1)
