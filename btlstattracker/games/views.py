# games/views.py
from flask import render_template,url_for,flash,redirect,request,Blueprint,session,jsonify
#from flask_login import login_user,current_user,logout_user,login_required
#from flask_user import current_user, roles_required
from btlstattracker import db
from btlstattracker.models import Games,GamesFromRiot,Players
from btlstattracker.games.forms import MatchInfo,TeamInfo,PlayerInfo
from btlstattracker.games.matchinfofunctions import getMatchInfo,getListOfPlayers, \
    getChampList,getTeamPlayers,convertToString,addInfoToPlayers,updateForSubs
import requests
import json
import pandas as pd
from flask_security import login_required,roles_required,current_user
#from btlstattracker.user.picture_handler import add_profile_pic

#TODO:Add Fill position for subs roles
games = Blueprint('games',__name__)

@games.route('/matchinfo',methods=['POST','GET'])
@login_required
@roles_required('admin')
def matchinfo():

    form = MatchInfo()
    if form.validate_on_submit():

        api = form.api.data
        match_id = form.match_id.data
        match_info = getMatchInfo(api,match_id)
        champ_list,champions_dict = getChampList(match_info)

        session['match_id'] = match_id
        session['season_number'] = form.season_number.data
        session['game_week'] = form.game_week.data
        #session['game_date'] = form.game_date.data
        session['champions_dict'] = champions_dict
        match_info = json.dumps(match_info)

        new_game = GamesFromRiot(match_id=match_id,game=match_info)
        db.session.add(new_game)
        db.session.commit()
        try:
            return redirect(url_for('games.teaminfo'))
        except:
            return redirect(url_for('core.index'))
    return render_template('matchinfo.html',form=form)

@games.route('/teaminfo',methods=['GET','POST'])
@login_required
@roles_required('admin')
def teaminfo():
    try:
        form = TeamInfo()

        teams = list(set([x.team for x in db.session.query(Players).all()]))
        form.blue_team.choices = teams
        form.red_team.choices = teams
        records_df,stats,stats_df = getListOfPlayers()
        session['records_df'] = records_df.to_dict('list')
        session['stats'] = stats
        if form.validate_on_submit():
            blue_team = form.blue_team.data
            red_team = form.red_team.data
            red_team_df,blue_team_df,sub_list,red_list,blue_list=getTeamPlayers(records_df,red_team,blue_team)
            session['red_team_df'] = red_team_df.to_dict()
            session['blue_team_df'] = blue_team_df.to_dict()
            session['red_list'] = red_list
            session['blue_list'] = blue_list
            return redirect(url_for('games.playerinfo'))
    except:
        print('not working')
    return render_template('teaminfo.html',form=form)

@games.route('/playerinfo',methods=['GET','POST'])
@login_required
@roles_required('admin')
def playerinfo():

    match_id = session.get('match_id')
    match_info = db.session.query(GamesFromRiot).filter(GamesFromRiot.match_id == match_id).first().game
    match_info = json.loads(match_info)
    champ_list,champions_dict = getChampList(match_info)
    sub_list = [x.summoner for x in db.session.query(Players).filter(Players.sub_or_player == 'Sub')]
    sub_list.insert(0,' ')
    week_number = session.get('week_number',None)
    season_number = session.get('season_number',None)
    red_team_df_dict = session.get('red_team_df',None)
    blue_team_df_dict = session.get('blue_team_df',None)
    red_team_df = pd.DataFrame.from_dict(red_team_df_dict)
    blue_team_df = pd.DataFrame.from_dict(blue_team_df_dict)
    stats = session.get('stats',None)

    form = PlayerInfo()
    #choices
    positions_dict = {'Blue Top':'blue_top','Blue Jungle':'blue_jungle','Blue Mid':'blue_middle',
                'Blue ADC':'blue_adc','Blue Support':'blue_support','Red Top':'red_top',
                'Red Jungle':'red_jungle','Red Mid':'red_middle','Red ADC':'red_adc',
                'Red Support':'red_support'}
    sub_dict = {'blue_top_sub':None,'blue_jungle_sub':None,'blue_middle_sub':None,
                'blue_adc_sub':None,'blue_support_sub':None,'red_top_sub':None,
                'red_jungle_sub':None,'red_middle_sub':None,'red_adc_sub':None,'red_support_sub':None}

    form.blue_top.choices = champ_list
    form.blue_jungle.choices = champ_list
    form.blue_middle.choices = champ_list
    form.blue_adc.choices = champ_list
    form.blue_support.choices = champ_list
    form.red_top.choices = champ_list
    form.red_jungle.choices = champ_list
    form.red_middle.choices = champ_list
    form.red_adc.choices = champ_list
    form.red_support.choices = champ_list

    form.blue_top_sub.choices = sub_list
    form.blue_jungle_sub.choices = sub_list
    form.blue_middle_sub.choices = sub_list
    form.blue_adc_sub.choices = sub_list
    form.blue_support_sub.choices = sub_list
    form.red_top_sub.choices = sub_list
    form.red_jungle_sub.choices = sub_list
    form.red_middle_sub.choices = sub_list
    form.red_adc_sub.choices = sub_list
    form.red_support_sub.choices = sub_list


    if form.validate_on_submit():

        positions_dict['Blue Top'] = form.blue_top.data
        positions_dict['Blue Jungle'] = form.blue_jungle.data
        positions_dict['Blue Mid'] = form.blue_middle.data
        positions_dict['Blue ADC'] = form.blue_adc.data
        positions_dict['Blue Support'] = form.blue_support.data
        positions_dict['Red Top'] = form.red_top.data
        positions_dict['Red Jungle'] = form.red_jungle.data
        positions_dict['Red Mid'] = form.red_middle.data
        positions_dict['Red ADC'] = form.red_adc.data
        positions_dict['Red Support'] = form.red_support.data

        sub_dict['blue_top_sub'] = form.blue_top_sub.data
        sub_dict['blue_jungle_sub'] = form.blue_jungle_sub.data
        sub_dict['blue_middle_sub'] = form.blue_middle_sub.data
        sub_dict['blue_adc_sub'] = form.blue_adc_sub.data
        sub_dict['blue_support_sub'] = form.blue_support_sub.data
        sub_dict['red_top_sub'] = form.red_top_sub.data
        sub_dict['red_jungle_sub'] = form.red_jungle_sub.data
        sub_dict['red_middle_sub'] = form.red_middle_sub.data
        sub_dict['red_adc_sub'] = form.red_adc_sub.data
        sub_dict['red_support_sub'] = form.red_support_sub.data

        red_team_df,blue_team_df = updateForSubs(sub_dict,red_team_df,blue_team_df)
        player_dict,teams_df = addInfoToPlayers(match_info,week_number,season_number,red_team_df,blue_team_df,stats,positions_dict,champions_dict)

        season_number = session.get('season_number')
        game_week_number = session.get('game_week')

        for index,row in teams_df.iterrows():
            game = Games(season = season_number,
                game_week = game_week_number,
                #game_date = session.get('game_date',None),
                game_id = match_id,
                summoner = row['Summoner'],
                role = row['Role'],
                team = row['Team'],
                sub_or_player = row['Sub or Player'],
                champion_id = row['championId'],
                game_duration = row['gameDuration'],
                ban_1 = row['ban 1'],
                ban_2 = row['ban 2'],
                ban_3 = row['ban 3'],
                ban_4 = row['ban 4'],
                ban_5 = row['ban 5'],
                win = row['win'],
                kills = row['kills'],
                deaths = row['deaths'],
                assists = row['assists'],
                total_damage_dealt = row['totalDamageDealt'],
                vision_score = row['visionScore'],
                gold_earned = row['goldEarned'],
                total_minions_killed = row['totalMinionsKilled'],
                first_blood_kill = row['firstBloodKill'],
                creeps_per_min_deltas_0_10 = row['creepsPerMinDeltas: 0-10'],
                creeps_per_min_deltas_10_20 = row['creepsPerMinDeltas: 10-20'],
                creeps_per_min_deltas_20_30 = row['creepsPerMinDeltas: 20-30'],
                creeps_per_min_deltas_30_end = row['creepsPerMinDeltas: 30-end'],
                gold_per_min_deltas_0_10 = row['goldPerMinDeltas: 0-10'],
                gold_per_min_deltas_10_20 = row['goldPerMinDeltas: 10-20'],
                gold_per_min_deltas_20_30 = row['goldPerMinDeltas: 20-30'],
                gold_per_min_deltas_30_end = row['goldPerMinDeltas: 30-end'])

            db.session.add(game)
            db.session.commit()
            session.clear()

            for key in list(session.keys()):
                 session.pop(key)
        return redirect(url_for('core.index'))
    return render_template('playerinfo.html',form=form)
