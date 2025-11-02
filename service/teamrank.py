from nba_api.stats.endpoints import leaguedashteamstats
import pandas as pd
import os

# 팀 로고 경로 반환 함수 (다운로드 폴더 기준)
def get_team_logo(team_name):
    image_urls = {
        "Atlanta Hawks": "https://i.imgur.com/h7ioTCE.png",
        "Boston Celtics": "https://i.imgur.com/1Ea6BBM.png",
        "Brooklyn Nets": "https://i.imgur.com/AlZfXGD.png",
        "Charlotte Hornets": "https://i.imgur.com/hP5DVfn.png",
        "Chicago Bulls": "https://i.imgur.com/4IaPK5U.png",
        "Cleveland Cavaliers": "https://i.imgur.com/kwe8R06.png",
        "Dallas Mavericks": "https://i.imgur.com/tkTfOBc.png",
        "Denver Nuggets": "https://i.imgur.com/JCDp4aT.png",
        "Detroit Pistons": "https://i.imgur.com/iD2NPhO.png",
        "Golden State Warriors": "https://i.imgur.com/F8EgNwJ.png",
        "Houston Rockets": "https://i.imgur.com/RRD8oA2.png",
        "Indiana Pacers": "https://i.imgur.com/chgEwvF.png",
        "Los Angeles Clippers": "https://i.imgur.com/ICu1svW.png",
        "Los Angeles Lakers": "https://i.imgur.com/r9hdFso.png",
        "Memphis Grizzlies": "https://i.imgur.com/zP9Svm9.png",
        "Miami Heat": "https://i.imgur.com/NnfBQGX.png",
        "Milwaukee Bucks": "https://i.imgur.com/VgYZwCM.png",
        "Minnesota Timberwolves": "https://i.imgur.com/CBK0ztn.png",
        "New Orleans Pelicans": "https://i.imgur.com/fI4tVb4.png",
        "New York Knicks": "https://i.imgur.com/KLRNiSh.png",
        "Oklahoma City Thunder": "https://i.imgur.com/DagCyxr.png",
        "Orlando Magic": "https://i.imgur.com/32jXpWA.png",
        "Philadelphia 76ers": "https://i.imgur.com/kWuPnFn.png",
        "Phoenix Suns": "https://i.imgur.com/Qd8t3n6.png",
        "Portland Trail Blazers": "https://i.imgur.com/pZtyNXW.png",
        "Sacramento Kings": "https://i.imgur.com/tD1LRKs.png",
        "San Antonio Spurs": "https://i.imgur.com/ueWwzz7.png",
        "Toronto Raptors": "https://i.imgur.com/U4WsWwJ.png",
        "Utah Jazz": "https://i.imgur.com/U734hhW.png",
        "Washington Wizards": "https://i.imgur.com/GMmgblP.png"
    }

    # 기본 로고 이미지 (없을 때 대비)
    default_url = "https://i.imgur.com/default_logo.png"
    return image_urls.get(team_name, default_url)


# 시즌별 팀 랭킹 반환
def get_season_team_rankings(season: str, top_n: int = 10):
    try:
        stats = leaguedashteamstats.LeagueDashTeamStats(season=season, season_type_all_star="Regular Season")

        excluded_team_ids = list(map(int, [
            "1611661314", "1611661315", "1611661321", "1611661316", "1611661320",
            "1611661324", "1611661313", "1611661323", "1611661317", "1611661318",
            "1610612760", "1611661319", "1611661322"
        ]))

        df = stats.get_data_frames()[0]
        df = df[~df['TEAM_ID'].isin(excluded_team_ids)]

        top_teams = df.sort_values(by='W_PCT', ascending=False).head(top_n)
        top_teams = top_teams[["TEAM_ID", "TEAM_NAME", "W", "L", "W_PCT"]]
        top_teams = top_teams.rename(columns={
            "TEAM_ID": "팀 ID",
            "TEAM_NAME": "팀 이름",
            "W": "승",
            "L": "패",
            "W_PCT": "승률"
        }).reset_index(drop=True)

        result_json = top_teams.to_dict(orient="records")
        for team in result_json:
            team["image_path"] = get_team_logo(team["팀 이름"])

        return result_json

    except Exception as e:
        return f"Error fetching data: {str(e)}"



