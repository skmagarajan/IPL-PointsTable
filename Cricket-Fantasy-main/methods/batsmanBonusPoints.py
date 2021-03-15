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