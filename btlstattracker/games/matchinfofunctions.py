import requests
import json
import pandas as pd
from btlstattracker import db
#from flask import jsonify

def getMatchInfo(api,matchId):
    matchInfo = requests.get('https://na1.api.riotgames.com/lol/match/v4/matches/{}?api_key={}'.format(matchId,api)).json()
    return matchInfo

def getListOfPlayers():
    #return as a dataframe
    stats = ['win','kills','deaths','assists','totalDamageDealt','visionScore','goldEarned',
         'totalMinionsKilled','firstBloodKill']
    timeline = ['creepsPerMinDeltas: 0-10','creepsPerMinDeltas: 10-20',
                'creepsPerMinDeltas: 20-30','creepsPerMinDeltas: 30-end',
                'goldPerMinDeltas: 0-10','goldPerMinDeltas: 10-20',
                'goldPerMinDeltas: 20-30','goldPerMinDeltas: 30-end',]
    other = ['championId','gameDuration','gameId','ban 1','ban 2','ban 3','ban 4','ban 5']

    stats_df = pd.DataFrame(columns = stats)
    records_df = pd.read_sql(sql = 'SELECT * FROM Players',con = db.session.bind,index_col =['id'] ,columns = ['Summoner','Role','Team','Sub or Player'])
    other_df = pd.DataFrame(columns = other)
    timeline_df = pd.DataFrame(columns = timeline)
    records_df = pd.concat((records_df,other_df,stats_df,timeline_df),axis=1)
    return records_df,stats,stats_df
#TODO: make champlist model

def getChampList(matchInfo):
    game_version = matchInfo['gameVersion'].split('.')
    patch_number = game_version[0]+'.'+game_version[1]+'.1'
    champ_json = requests.get('http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion.json'.format(patch_number)).json()

    champions_dict = {}
    champ_json_data = champ_json['data']

    for champ in champ_json_data:
        champions_dict[champ] = champ_json_data[champ]['key']
    champ_list = []
    for k,v in champions_dict.items():
        champ_list.append(k)
    return champ_list,champions_dict


########################################################################################

#TODO: need to make a teams, players model/df that is stored elsewhere to then reference when needed
def getTeamPlayers(records_df,redSideTeam,blueSideTeam):
#take in dataframe of listofPlayers
#assign redSideTeam from dataframe to red team
#assign blueSideTeam from dataframe to blue team
#update dataframe
#[['Summoner','Role']]
    sub_df = records_df[records_df['Sub or Player']=='Sub']['Summoner']
    red_team_df = records_df[records_df['Team']==redSideTeam]
    blue_team_df = records_df[records_df['Team']==blueSideTeam]
    sub_list = list(sub_df)
    red_list = list(red_team_df)
    blue_list = list(blue_team_df)
    all_sums_list = red_list+blue_list
    return red_team_df,blue_team_df,sub_list,red_list,blue_list

def updateForSubs(sub_dict,red_team_df,blue_team_df):
    for subs in sub_dict:
        for index,row in red_team_df.iterrows():
            if (subs.split('_')[1].lower() == row['Role'].lower()) & (subs.split('_')[0].lower() == 'red') & (sub_dict[subs] != ' '):
                row['Summoner'] = sub_dict[subs]
        for index,row in blue_team_df.iterrows():
            if (subs.split('_')[1].lower() == row['Role'].lower()) & (subs.split('_')[0].lower() == 'blue') & (sub_dict[subs] != ' '):
                row['Summoner'] = sub_dict[subs]
    return red_team_df,blue_team_df

def convertToString(positions_dict):
    for i in positions_dict:
        positions_dict = i.get()
    return positions_dict

def addInfoToPlayers(matchInfo,week_number,season_number,red_team_df,blue_team_df,stats,positions_dict,champions_dict):
    player = {}
    deltas = ['0-10','10-20','20-30','30-end']
    gameDuration = matchInfo['gameDuration']
    gameId = matchInfo['gameId']
    bans = {'ban 1':None,'ban 2':None,'ban 3':None,'ban 4':None,'ban 5':None}
    red_banned_champions = matchInfo['teams'][0]['bans']
    blue_banned_champions = matchInfo['teams'][1]['bans']

    for i in matchInfo['participants']:
        for champ,number in champions_dict.items():
            if str(i.get('championId')) == number:
                player[champ] = i
            else:
                pass
    player_dict = {k: player.get(v) for k,v in positions_dict.items()}

    for x in red_team_df.index:
        if red_team_df['Role'][x] == 'Sub':
            continue
        a = player_dict['Red '+ red_team_df['Role'][x]]['stats']
        for stat in stats:
           red_team_df[stat][x] = a[stat]

    for x in blue_team_df.index:
        if blue_team_df['Role'][x] == 'Sub':
            continue
        a = player_dict['Blue '+ blue_team_df['Role'][x]]['stats']
        for stat in stats:
           blue_team_df[stat][x] = a[stat]

    for x in red_team_df.index:
        try:
            if red_team_df['Role'][x] == 'Sub':
                continue
            for delta in deltas:
                a = player_dict['Red '+ red_team_df['Role'][x]]['timeline']['creepsPerMinDeltas'][delta]
                red_team_df['creepsPerMinDeltas: {}'.format(delta)][x] = a
        except KeyError:
            continue

    for x in blue_team_df.index:
        try:
            if blue_team_df['Role'][x] == 'Sub':
                continue
            for delta in deltas:
                a = player_dict['Blue '+ blue_team_df['Role'][x]]['timeline']['creepsPerMinDeltas'][delta]
                blue_team_df['creepsPerMinDeltas: {}'.format(delta)][x] = a
        except KeyError:
            continue

    for x in red_team_df.index:
        try:
            if red_team_df['Role'][x] == 'Sub':
                continue
            for delta in deltas:
                a = player_dict['Red '+ red_team_df['Role'][x]]['timeline']['goldPerMinDeltas'][delta]
                red_team_df['goldPerMinDeltas: {}'.format(delta)][x] = a
        except KeyError:
            continue

    for x in blue_team_df.index:
        try:
            if blue_team_df['Role'][x] == 'Sub':
                continue
            for delta in deltas:
                a = player_dict['Blue '+ blue_team_df['Role'][x]]['timeline']['goldPerMinDeltas'][delta]
                blue_team_df['goldPerMinDeltas: {}'.format(delta)][x] = a
        except KeyError:
            continue

    for x in red_team_df.index:
        if red_team_df['Role'][x] == 'Sub':
                continue
        a = player_dict['Red '+ red_team_df['Role'][x]]['championId']
        for champ,number in champions_dict.items():
            if str(number) == str(a):
                a = champ
        red_team_df['championId'][x] = a

        red_team_df['gameDuration'][x] = gameDuration

        for i in range(0,5):
            try:
                bans['ban {}'.format(i+1)] = red_banned_champions[i]['championId']
            except:
                bans['ban {}'.format(i+1)] = 'None'
        for ban_number,ban in bans.items():
            for champs,numbers in champions_dict.items():
                if str(numbers) == str(ban):
                    ban = champs
            red_team_df[ban_number][x] = ban

        red_team_df['gameId'][x] = gameId

    for x in blue_team_df.index:
        if blue_team_df['Role'][x] == 'Sub':
                continue
        a = player_dict['Blue '+ blue_team_df['Role'][x]]['championId']
        for champ,number in champions_dict.items():
            if str(number) == str(a):
                a = champ
        blue_team_df['championId'][x] = a

        blue_team_df['gameDuration'][x] = gameDuration

        for i in range(0,5):
            try:
                bans['ban {}'.format(i+1)] = blue_banned_champions[i]['championId']
            except:
                bans['ban {}'.format(i+1)] = 'None'
        for ban_number,ban in bans.items():
            for champs,numbers in champions_dict.items():
                if str(numbers) == str(ban):
                    ban = champs
            blue_team_df[ban_number][x] = ban

        blue_team_df['gameId'][x] = gameId


    teams_df=pd.concat([red_team_df,blue_team_df])
    teams_df['Season'] = season_number
    teams_df['Week'] = week_number
    return player_dict,teams_df
