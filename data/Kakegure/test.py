from riotwatcher import LolWatcher, ApiError
import pandas as pds
import numpy as num
import champion_reader as cr
from pathlib import Path
import os
import csv

# golbal variables
api_key = 'RGAPI-c273c4c5-5dcc-4319-bbb8-3161ab685d0c'
watcher = LolWatcher(api_key)
my_region = 'na1'

# Testing known summoner
me = watcher.summoner.by_name(my_region, 'Kaminaryuu')

# Return the rank status for Me
my_ranked_stats = watcher.league.by_summoner(my_region, me['id'])

# Return Last 100 Matches Recorded
matches = watcher.match.matchlist_by_puuid(my_region, me['puuid'], 0, 100)

# Analyzing Last Match
last_match = matches[1]

# Getting the data from last match in dictionary format
match_detail = watcher.match.by_id(my_region, last_match)

# Removing info and metadata keys - no needed
remove_info = match_detail.pop('metadata')
remove_info = match_detail.pop('info')

# Getting List of Participants
participants = remove_info.get('participants')

# Champion and ID Data Frame - ci_df
ci_df = cr.Champ_Frame

# Game, Player and Combined Dictionaries
gameData = []
playerData = []
comb = {}
# Game Counter
gc = 0
# Validation of Ranked Games (Solo Queue only)
sq = False

# First, iterate through the game data to find the queue ID
# to know whether we want this data or not
for row in remove_info:
    # Game Data
    gd = {}

    # Identifying the Queue Type for regular games
    if row == 'queueId':
        # Solo Queue Games
        if remove_info[row] == 420:
            sq = True
            gd['Queue Type'] = "Solo Queue"
            gameData.append(gd)
        
        # Flex Queue Games (future application)
        if remove_info[row] == 440:
            sq = True
            gd['Queue Type'] = "Flex Queue"
            gameData.append(gd)

    # For Scrims
    if row == 'Game Mode':
        if remove_info[row] == 'CUSTOM':
            gd['Game Mode'] = remove_info[row]
            gameData.append(gd)
            sq = True

# Now to Retrieve the actual Game Data
for row in remove_info:
    # Game Data
    gd = {}
    # First retrieve Game Type and Mode
    if row == 'gameDuration':
        gd['Game Duration'] = remove_info[row]
        gameData.append(gd)
    if row == 'gameType':
        gd['Game Type'] = remove_info[row]
        gameData.append(gd)
    if row == 'gameMode':
        gd['Game Mode'] = remove_info[row]
        gameData.append(gd)

    if sq is True:
        # Game Data is inside Participants Key
        if row == 'participants':
            # Local Varialbe for the new Dictionary to be traversed
            LL = remove_info[row]

            # Traversing Each Player Data (pd) on the Game        
            for pd in remove_info[row]:
                # Player Data local variable
                pdll = {}

                # Some data that we want is under another dictionary called
                # challenges. Before that iteration, we will take the data we want
                # from the keys that are accessible from here

                # Player, Champion Selection, Lane and Role
                summonerName = pd.get('summonerName')
                champSelected = pd.get('championName')
                # for Wukong
                if champSelected == 'MonkeyKing':
                    champSelected = 'Wukong'
                if pd.get('teamPosition') == 'UTILITY':
                    lane = 'SUPPORT'
                else:
                    lane = pd.get('teamPosition')

                # Champion Data
                champLevel = pd.get('champLevel')
                kills = pd.get('kills')
                assists = pd.get('assists')
                deaths = pd.get('deaths')
                
                # Performance Metrics In General
                triple = pd.get('tripleKills')
                quadra = pd.get('quadraKills')
                penta = pd.get('pentaKills')
                objetivesStolen = pd.get('objectivesStolen')
                firstBlood = pd.get('firstBloodKill')

                # Total Damage Chart
                damageToChamp = pd.get('totalDamageDealtToChampions')
                damageTaken = pd.get('totalDamageTaken')

                # Gold Chart
                totalGold = pd.get('goldEarned')

                # Warding and vision score
                wardPlaced = pd.get('wardsPlaced')
                wardKilled = pd.get('wardsKilled')
                wardBought = pd.get('visionWardsBoughtinGame')
                vs = pd.get('visionScore')
                
                # Time Statistics
                totalTimeCCing = pd.get('totalTimeCCDealt')
                timeDead = pd.get('totalTimeSpentDead')
                
                # Game Results
                timePlayed = pd.get('timePlayed')
                result = pd.get('win')

                # Turret Information
                turretTakedowns = pd.get('turretTakedowns')
                damageDealtToTurrets = pd.get('damageDealtToTurrets')
                turretKills = pd.get('turretKills')
                firstTurret = pd.get('firstTowerKill')
                turretLost = pd.get('turretsLost')

                # Surrender
                gameSurrenders = pd.get('gameEndedInSurrender')
                teamEarlySurrender = pd.get('teamEarlySurrendered')

                # Total CS Data
                laneCS = pd.get('totalMinionsKilled')
                neutralCS = pd.get('neutralMinionsKilled')

                # Retrieving Dict of Challenges
                challenges = pd.get('challenges')

                # Getting data from Challenges
                gpm = challenges.get('goldPerMinute')
                cward = challenges.get('controlWardsPlaced')
                dpm = challenges.get('damagePerMinute')
                teamDamageTakenPercentage = round(challenges.get('damageTakenOnTeamPercentage') * 100, 2)
                kda = round(challenges.get('kda'), 2)
                divesReceived = challenges.get('killsUnderOwnTurret')
                kp = challenges.get('killParticipation') * 100
                divesPerformed = challenges.get('killsNearEnemyTurret')
                teamDamagePercentage = round(challenges.get('teamDamagePercentage') * 100, 2)
                earlyTurrets = challenges.get('outerTurretExecutesBefore10Minutes')
                turretPlatesTaken = challenges.get('turretPlatesTaken')
                vpm = challenges.get('visionScorePerMinute')
                wardTakendowns20 = challenges.get('wardTakedownsBefore20M')
                turretWithHerald = challenges.get('turretsTakenWithRiftHerald')
                soloKill = challenges.get('soloKills')
                allyJG = challenges.get('alliedJungleMonsterKills')
                enemyJG = challenges.get('enemyJungleMonsterKills')

                # Jungle vs Lane CS                        
                if lane == 'JUNGLE':
                    cs10 = round(challenges.get('jungleCsBefore10Minutes'))
                    goldDiff10 = challenges.get('laningPhaseGoldExpAdvantage')
                else:
                    cs10 = round(challenges.get('laneMinionsFirst10Minutes'))
                    goldDiff10 = challenges.get('earlyLaningPhaseGoldExpAdvantage')

                # We now calculate the correct CS for each player
                cs = laneCS + neutralCS + round(allyJG) + round(enemyJG)
                cs = round(cs, 2)

                # Time Played is collected in seconds, so we need to convert into minutes
                minutes = timePlayed / 60
                seconds = timePlayed % 60
                minQuotient = timePlayed // 60
                # Therefore, CS per minute is
                csm = cs / minutes

                # Converting into string data
                minSTR = str(minQuotient)
                minSEC = str(seconds).zfill(2)
                gameTime = minSTR + ':' + minSEC

                # Creating Player Data Dictionary
                pdll['Summoner Name'] = summonerName
                pdll['Champion Selected'] = champSelected
                pdll['Lane'] = lane
                pdll['Champion Level'] = champLevel
                pdll['Kills'] = kills
                pdll['Deaths'] = deaths
                pdll['Assists'] = assists
                pdll['KDA'] = kda
                pdll['Damage Per Minute'] = dpm
                pdll['Gold Per Minute'] = gpm
                pdll['Vision Score Per Minute'] = vpm
                pdll['Triple Kills'] = triple
                pdll['Quadra Kills'] = quadra
                pdll['Penta Kills'] = penta
                pdll['Number of Solo Kills'] = soloKill
                pdll['Kill Participation'] = kp
                pdll['CS@10'] = cs10
                pdll['GD@10'] = goldDiff10
                pdll['Damage to Champion'] = damageToChamp
                pdll['Damage Taken'] = damageTaken
                pdll['Team Damage Dealt Percentage'] = teamDamagePercentage
                pdll['Team Damage Taken Percentage'] = teamDamageTakenPercentage
                pdll['Total Gold Earned'] = totalGold
                pdll['Control Wards Placed'] = cward
                pdll['Wards Placed'] = wardPlaced
                pdll['Wards Killed'] = wardKilled
                pdll['Control Wards Bought'] = wardBought
                pdll['Vision Score'] = vs
                pdll['Total CC Time Dealt'] = totalTimeCCing
                pdll['Total Time Spent Dead'] = timeDead
                pdll['Game Ended in Surrender'] = gameSurrenders
                pdll['Own Team Early Surrender'] = teamEarlySurrender
                pdll['Time Played '] = gameTime
                pdll['Win'] = result
                pdll['Total CS'] = cs
                pdll['CS Per Minute'] = csm
                pdll['Turrets Taken with Herald'] = turretWithHerald
                pdll['Turrets Takedowns'] = turretTakedowns
                pdll['Plates Taken'] = turretPlatesTaken
                pdll['Damage to Turrets'] = damageDealtToTurrets
                pdll['Turrets Taken'] = turretKills
                pdll['Turrets Lost'] = turretLost
                pdll['Turrets Taken Before 10min'] = earlyTurrets
                pdll['Dives Received'] = divesReceived
                pdll['Dives Taken'] = divesPerformed
                pdll['Objectives Stolen'] = objetivesStolen
                pdll['First Turret'] = firstTurret
                pdll['First Blood'] = firstBlood
                pdll['Ward Take Downs Before 20min'] = wardTakendowns20

                # Saving all in Game Data
                playerData.append(pdll)

        else:
            # Clear memory from gd dictionary if not a ranked game
            gd.clear()


    # Section reserved to retrieve data from pick/ban phase
    if row == 'teams':
        # 
        keys = remove_info[row].keys()
        print(keys)

# Combining the two Dictonarys
comb['Game Data'] = gameData
comb['Player Data'] = playerData

# Creating a Data Frame for Game Data
playerDF = pds.DataFrame(comb['Player Data'])

# If Data Frame is empty, clear it and dont use it.
# If there is data on it, save it
if playerDF.empty:
    # Clear Memory and return nothing
    comb.clear()
    gameData.clear()
    playerData.clear()
else:
    # File Name and Saving in Excel
    #file_name = 'Game_Data.xlsx'
    #playerDF.to_excel(file_name)

    # Clearing Memory
    comb.clear()
    gameData.clear()
    playerData.clear()
    playerDF.drop(playerDF.index, inplace=True)