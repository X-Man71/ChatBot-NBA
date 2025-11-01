from nba_api.stats.endpoints import leaguedashplayerstats
import pandas as pd
from nba_api.stats.static import players

def get_player_id(player_name):
    nba_players = players.get_players()
    for player in nba_players:
        if player['full_name'].lower() == player_name.lower():
            return player['id']
    return None

def get_player_image(player_name):
    player_id = get_player_id(player_name)
    if player_id:
        return f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player_id}.png"
    else:
        return "https://cdn-icons-png.flaticon.com/512/847/847969.png"
    
def get_season_player_rankings(season: str, top_n: int = 10, stat: str = "PTS"):
    try:
        stats = leaguedashplayerstats.LeagueDashPlayerStats(season=season)
        df = stats.get_data_frames()[0]

        # 주요 통계 기준 내림차순 정렬 후 상위 top_n 추출
        top_players = df.sort_values(by=stat, ascending=False).head(top_n)

        # 필요한 열만 추출하고 컬럼명 한글로 변경
        top_players = top_players[["PLAYER_NAME", "TEAM_ABBREVIATION", "GP", stat]]
        top_players = top_players.rename(columns={
            "PLAYER_NAME": "선수 이름",
            "TEAM_ABBREVIATION": "팀",
            "GP": "경기수",
            stat: stat
        })
        top_players = top_players.reset_index(drop=True)

        # JSON 형태로 변환
        result_json = top_players.to_dict(orient="records")
        for player in result_json:
            player_name = player["선수 이름"]
            player["image_url"] = get_player_image(player_name)

        return result_json

    except Exception as e:
        return f"Error fetching data: {str(e)}"
