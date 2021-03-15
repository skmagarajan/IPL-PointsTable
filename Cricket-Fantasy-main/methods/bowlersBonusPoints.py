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