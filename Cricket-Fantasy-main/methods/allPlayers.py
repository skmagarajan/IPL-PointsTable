def allPlayers(team, playerTemplate):
    players = {}
    for p in team:
        player = playerTemplate.copy()
        pid = p['href'][10:]
        pid = str(pid[:pid.find('/')])
        players[pid] = player

    return players