import requests
from bs4 import BeautifulSoup
import json
import os
import sys

def allPlayers(team, playerTemplate):
    players = {}
    for p in team:
        player = playerTemplate.copy()
        pid = p['href'][10:]
        pid = str(pid[:pid.find('/')])
        players[pid] = player

    return players

def batsmanBonusPoints(runs, out, balls, sRate):
    runsPoints = 0
    if runs >= 50 and runs < 100:
        runsPoints = 8
    elif runs >= 100:
        runsPoints = 16
    elif runs == 0 and out != 'not out':
        runsPoints = -2
    else:
        runsPoints = 0
    
    srPoints = 0
    if balls >= 10:
        if sRate >= 60 and sRate <= 70:
            srPoints = -2
        elif sRate >= 50 and sRate <= 59.99:
            srPoints = -4
        elif sRate < 50:
            srPoints = -6
    
    return runsPoints + srPoints

def bowlersBonusPoints(wickets, maidens, overs, economy):
    wicketsPoints = 0
    if wickets == 3:
        wicketsPoints = 8
    elif wickets == 5:
        wicketsPoints = 16
    
    economyPoints = 0
    if overs >= 2:
        if economy <= 4:
            economyPoints = 6
        elif economy > 4 and economy <= 4.99:
            economyPoints = 4
        elif economy >= 5 and economy <= 6:
            economyPoints = 2
        elif economy >= 9 and economy <= 10:
            economyPoints = -2
        elif economy >= 10.01 and economy <= 11:
            economyPoints = -4
        elif economy > 11:
            economyPoints = -6

    return wicketsPoints + economyPoints + (maidens * 8)

def catches(battingInfo):
    outInfo = []
    for p in battingInfo:
        if p != 'not out':
            outInfo.append(p)

    removedC = []
    for o in outInfo:
        try:
            removedC.append(o.split('c ')[1])
        except IndexError:
            removedC.append(o.split('c ')[0])

    removedB = []
    for c in removedC:
        removedB.append(c.split('b ')[0])
    removedB = [b.strip(' ') for b in removedB]

    catchesTakenBy = []
    for b in removedB:
        if 'run out' not in b:
            catchesTakenBy.append(b)
            
    catchesTakenBy = [x for x in catchesTakenBy if x != '']
    catchesTakenBy = [x for x in catchesTakenBy if len(x) > 1]
    catchesTakenBy = [x.replace('(sub)', '') for x in catchesTakenBy]

    return catchesTakenBy

def dataToBatsman(batsmanInfo, players):
    for p in batsmanInfo:
        if p['pid'] in players:
            players[p['pid']]['pid'] = p['pid']
            players[p['pid']]['name'] = p['name']
            try:
                players[p['pid']]['runsScored'] = p['runsScored']
                players[p['pid']]['out'] = False if p['out'] == 'not out' else True
                players[p['pid']]['ballsFaced'] = p['balls']
                players[p['pid']]['fours'] = p['fours']
                players[p['pid']]['sixes'] = p['sixes']
                players[p['pid']]['strikeRate'] = p['sr']
                players[p['pid']]['catches'] = p['catches']
                players[p['pid']]['runouts'] = p['runouts']
                players[p['pid']]['stumpings'] = p['stumpings']
                
                players[p['pid']]['points'] = int(p['runsScored']) + int(p['fours']) + (int(p['sixes']) * 2) + batsmanBonusPoints(int(p['runsScored']), p['out'], int(p['balls']), float(p['sr'])) + (p['catches'] * 8) + (p['runouts'] * 8) + (p['stumpings'] * 12)
            except KeyError:
                pass
    
    return players

def dataToBowlers(bowlersInfo, players):
    for p in bowlersInfo:
        if p['pid'] in players:
            players[p['pid']]['pid'] = p['pid']
            players[p['pid']]['name'] = p['name']
            players[p['pid']]['overs'] = p['overs']
            players[p['pid']]['maidens'] = p['maidens']
            players[p['pid']]['runsGiven'] = p['runsGiven']
            players[p['pid']]['wickets'] = p['wickets']
            players[p['pid']]['noBalls'] = p['no_balls']
            players[p['pid']]['wides'] = p['wides']
            players[p['pid']]['economy'] = p['economy']
            players[p['pid']]['catches'] = p['catches']
            players[p['pid']]['runouts'] = p['runouts']

            try:
                players[p['pid']]['points'] = players[p['pid']]['points'] + (int(p['wickets']) * 25) + bowlersBonusPoints(int(p['wickets']), int(p['maidens']), float(p['overs']), float(p['economy'])) + (p['catches'] * 8) + (p['runouts'] * 8)
            except KeyError:
                players[p['pid']]['points'] = (int(p['wickets']) * 25) + bowlersBonusPoints(int(p['wickets']), int(p['maidens']), float(p['overs']), float(p['economy'])) + (p['catches'] * 8) + (p['runouts'] * 8)

    return players

def formDict(data):
    return {x:data.count(x) for x in data}

def getBattingInfo(bat, firstInnCatches, firstInnRunouts, firstInnStumpings, secondInnCatches, secondInnRunouts, secondInnStumpings):
    batsmanInfo = []
    remove = 'Did not Bat'
    for b in bat:
        if remove not in b.get_text():
            batsman = {}
            name = b.find('a', class_='cb-text-link')
            if name:
                pid = name['href'][10:]
                batsman['pid'] = str(pid[:pid.find('/')])
                batsman['name'] = str(name.get_text().strip())
                if '(' in batsman['name']:
                    batsman['name'] = batsman['name'][:batsman['name'].find('(')].strip()
                batsman['catches'] = 0
                batsman['runouts'] = 0
                batsman['stumpings'] = 0
                
                for key in firstInnCatches.keys():
                    if key in batsman['name']:
                        batsman['catches'] = firstInnCatches[key]
                for key in secondInnCatches.keys():
                    if key in batsman['name']:
                        batsman['catches'] = secondInnCatches[key]
                for key in firstInnRunouts.keys():
                    if key in batsman['name']:
                        batsman['runouts'] = firstInnRunouts[key]
                for key in secondInnRunouts.keys():
                    if key in batsman['name']:
                        batsman['runouts'] = secondInnRunouts[key]
                for key in firstInnStumpings.keys():
                    if key in batsman['name']:
                        batsman['stumpings'] = firstInnStumpings[key]
                for key in secondInnStumpings.keys():
                    if key in batsman['name']:
                        batsman['stumpings'] = secondInnStumpings[key]

                try:
                    batsman['out'] = b.find('span', class_='text-gray').get_text().strip()
                    batsman['runsScored'] = b.find('div', class_='cb-col cb-col-8 text-right text-bold').get_text()
                    batsman['balls'] = b.find_all('div', class_='cb-col cb-col-8 text-right')[0].get_text()
                    batsman['fours'] = b.find_all('div', class_='cb-col cb-col-8 text-right')[1].get_text()
                    batsman['sixes'] = b.find_all('div', class_='cb-col cb-col-8 text-right')[2].get_text()
                    batsman['sr'] = b.find_all('div', class_='cb-col cb-col-8 text-right')[3].get_text()
                except AttributeError:
                    pass
        
        if batsman:
            batsmanInfo.append(batsman)
                    
    return batsmanInfo

def getBowlingInfo(bowl, firstInnCatches, firstInnRunouts, secondInnCatches, secondInnRunouts):
    bowlerInfo = []
    for b in bowl:
        bowler = {}
        name = b.find('a', class_='cb-text-link')
        if name:
            pid = name['href'][10:]
            bowler['pid'] = str(pid[:pid.find('/')])
            bowler['name'] = str(name.get_text().strip())
            if '(' in bowler['name']:
                bowler['name'] = bowler['name'][:bowler['name'].find('(')].strip()
            bowler['catches'] = 0
            bowler['runouts'] = 0
            bowler['stumpings'] = 0
                
            for key in firstInnCatches.keys():
                if key in bowler['name']:
                    bowler['catches'] = firstInnCatches[key]
            for key in secondInnCatches.keys():
                if key in bowler['name']:
                    bowler['catches'] = secondInnCatches[key]
            for key in firstInnRunouts.keys():
                if key in bowler['name']:
                    bowler['runouts'] = firstInnRunouts[key]
            for key in secondInnRunouts.keys():
                if key in bowler['name']:
                    bowler['runouts'] = secondInnRunouts[key]

            bowler['overs'] = b.find_all('div', class_='cb-col cb-col-8 text-right')[0].get_text()
            bowler['maidens'] = b.find_all('div', class_='cb-col cb-col-8 text-right')[1].get_text()
            bowler['runsGiven'] = b.find_all('div', class_='cb-col cb-col-10 text-right')[0].get_text()
            bowler['wickets'] = b.find('div', class_='cb-col cb-col-8 text-right text-bold').get_text()
            bowler['no_balls'] = b.find_all('div', class_='cb-col cb-col-8 text-right')[2].get_text()
            bowler['wides'] = b.find_all('div', class_='cb-col cb-col-8 text-right')[3].get_text()
            bowler['economy'] = b.find_all('div', class_='cb-col cb-col-10 text-right')[1].get_text()
        
        if bowler:
            bowlerInfo.append(bowler)

    return bowlerInfo

def innOutBy(innBat):
    outBy = []
    for f in innBat:
        try:
            outBy.append(f.find('span', class_='text-gray').get_text().strip())
        except AttributeError:
            pass
    
    return outBy

def runouts(battingInfo):
    outInfo = []
    for p in battingInfo:
        if p != 'not out':
            outInfo.append(p)

    removedC = []
    for o in outInfo:
        try:
            removedC.append(o.split('c ')[1])
        except IndexError:
            removedC.append(o.split('c ')[0])

    removedB = []
    for c in removedC:
        removedB.append(c.split('b ')[0])
    removedB = [b.strip(' ') for b in removedB]
    
    r = []
    for b in removedB:
        if 'run out' in b and 'sub' not in b:
            r.append(b)

    runoutsDoneBy = []
    for x in r:
        try:
            runoutsDoneBy.append((x.split('(')[1]).split('/')[0])
            runoutsDoneBy.append(((x.split('(')[1]).split('/')[1]).split(')')[0])
        except IndexError:
            runoutsDoneBy.append((x.split('(')[1]).split(')')[0])
    runoutsDoneBy = [x for x in runoutsDoneBy if ')' not in x]

    return runoutsDoneBy

def stumpings(battingInfo):
    stumpingInfo = []
    for p in battingInfo:
        if p != 'not out' and p.startswith('st'):
            stumpingInfo.append(p)
    
    stumpingsDoneBy = []
    for s in stumpingInfo:
        stumpingsDoneBy.append(s.split('st ')[1].split(' b')[0])
    
    return stumpingsDoneBy

# with open('./Cricket-Fantasy-main/matchURLs.txt') as f:
#     URLs = []
#     for line in f:
#         URLs.append(line.strip())

URL = sys.argv[1]

scoreCard = requests.get(URL).text
soup = BeautifulSoup(scoreCard, 'html.parser')

playerTemplate = {
    "pid": "0",
    "name": "",
    "runsScored": "0",
    "ballsFaced": "0",
    "fours": "0",
    "sixes": "0",
    "strikeRate": "0",
    "out": False,
    "overs": "0",
    "maidens": "0",
    "runsGiven": "0",
    "wickets": "0",
    "noBalls": "0",
    "wides": "0",
    "economy": "0",
    "catches": 0,
    "runouts": 0,
    "stumpings": 0
}

firstInn = soup.find_all('div', id='innings_1')[0]
firstInnBat = firstInn.find_all('div', class_='cb-col cb-col-100 cb-ltst-wgt-hdr')[0]
firstInnBat = firstInnBat.find_all('div', class_='cb-col cb-col-100 cb-scrd-itms')
firstInnBowl = firstInn.find_all('div', class_='cb-col cb-col-100 cb-ltst-wgt-hdr')[1]
firstInnBowl = firstInnBowl.find_all('div', class_='cb-col cb-col-100 cb-scrd-itms')
firstInnScore = firstInn.find('span', class_='pull-right').get_text().split(' ')[0]
firstInnTeam = firstInn.find('span').get_text()
firstInnTeam = firstInnTeam[:firstInnTeam.find(' Innings')]

secondInn = soup.find_all('div', id='innings_2')[0]
secondInnBat = secondInn.find_all('div', class_='cb-col cb-col-100 cb-ltst-wgt-hdr')[0]
secondInnBat = secondInnBat.find_all('div', class_='cb-col cb-col-100 cb-scrd-itms')
secondInnBowl = secondInn.find_all('div', class_='cb-col cb-col-100 cb-ltst-wgt-hdr')[1]
secondInnBowl = secondInnBowl.find_all('div', class_='cb-col cb-col-100 cb-scrd-itms')
secondInnScore = secondInn.find('span', class_='pull-right').get_text().split(' ')[0]
secondInnTeam = secondInn.find('span').get_text()
secondInnTeam = secondInnTeam[:secondInnTeam.find(' Innings')]

firstInnCatches = catches(innOutBy(firstInnBat))
firstInnCatches = formDict(firstInnCatches)
secondInnCatches = catches(innOutBy(secondInnBat))
secondInnCatches = formDict(secondInnCatches)

firstInnRunouts = runouts(innOutBy(firstInnBat))
firstInnRunouts = formDict(firstInnRunouts)
secondInnRunouts = runouts(innOutBy(secondInnBat))
secondInnRunouts = formDict(secondInnRunouts)

firstInnStumpings = stumpings(innOutBy(firstInnBat))
firstInnStumpings = formDict(firstInnStumpings)
secondInnStumpings = stumpings(innOutBy(secondInnBat))
secondInnStumpings = formDict(secondInnStumpings)

firstInnBatInfo = getBattingInfo(firstInnBat, firstInnCatches, firstInnRunouts, firstInnStumpings, secondInnCatches, secondInnRunouts, secondInnStumpings)
secondInnBatInfo = getBattingInfo(secondInnBat, firstInnCatches, firstInnRunouts, firstInnStumpings, secondInnCatches, secondInnRunouts, secondInnStumpings)

firstInnBowlInfo = getBowlingInfo(firstInnBowl, firstInnCatches, firstInnRunouts, secondInnCatches, secondInnRunouts)
secondInnBowlInfo = getBowlingInfo(secondInnBowl, firstInnCatches, firstInnRunouts, secondInnCatches, secondInnRunouts)

playingXI = soup.find_all('div', class_='cb-col cb-col-100 cb-minfo-tm-nm')
team = playingXI[1].find_all('a') + playingXI[3].find_all('a')
players = allPlayers(team, playerTemplate)

players = dataToBatsman(firstInnBatInfo, players)
players = dataToBatsman(secondInnBatInfo, players)
players = dataToBowlers(firstInnBowlInfo, players)
players = dataToBowlers(secondInnBowlInfo, players)

if not os.path.isfile('./Cricket-Fantasy-main/points/seasonPoints.json'):
    dumpPlayers = {}
    for key in players:
        try:
            dumpPlayers[players[key]['pid']] = {'name': players[key]['name'], 'points': players[key]['points']}
        except KeyError:
            pass
    
    with open('./Cricket-Fantasy-main/points/seasonPoints.json', 'w') as f:            
        json.dump(dumpPlayers, f, indent=4)

else:
    with open('./Cricket-Fantasy-main/points/seasonPoints.json', 'r') as f:
        existPlayers = json.load(f)

    for key in players:
        if key in existPlayers:
            try:
                existPlayers[key]['points'] += players[key]['points']   
            except KeyError:
                pass
        else:
            try:
                existPlayers[players[key]['pid']] = {'name': players[key]['name'], 'points': players[key]['points']}
            except KeyError:
                pass
    
    with open('./Cricket-Fantasy-main/points/seasonPoints.json', 'w') as f:
        json.dump(existPlayers, f, indent=4)

matchFileName = URL.split('/')[5]

with open('./Cricket-Fantasy-main/points/matchPoints/' + matchFileName + '.json', 'w') as f:
    json.dump(players, f, indent=4)
    print(matchFileName + ' is done!')