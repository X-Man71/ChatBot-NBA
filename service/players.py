from nba_api.stats.static import players

def get_all_players(page=1):
    all_players = players.get_players()
    lst = []
    page = int(page)
    for i in range(50*page, (50*page)+50):
        lst.append(all_players[i])
    return lst

def get_players_by_name(name):
    info = players.find_players_by_full_name(name)
    return info
