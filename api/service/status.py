from nba_api.stats.endpoints import leaguedashplayerstats
import pandas as pd

def get_season_player_stats(season: str, top_n: int = 10):
    """
    특정 시즌의 선수별 주요 능력치를 반환하는 함수입니다.

    Parameters:
    - season (str): 시즌 형식은 '2024-25'
    - top_n (int): 득점 기준 상위 N명의 선수 표시

    Returns:
    - pandas.DataFrame: 선수 이름, 팀, 경기 수, 평균 득점, 리바운드, 어시스트, 스틸, 블락 포함
    """
    try:
        stats = leaguedashplayerstats.LeagueDashPlayerStats(season=season)
        df = stats.get_data_frames()[0]

        # 득점(PTS) 기준 내림차순 정렬 후 상위 N명 추출
        top_players = df.sort_values(by='PTS', ascending=False).head(top_n)

        # 필요한 열만 추출
        result = top_players[[
            "PLAYER_NAME", "TEAM_ABBREVIATION", "GP",
            "PTS", "REB", "AST", "STL", "BLK"
        ]]
        result = result.rename(columns={
            "PLAYER_NAME": "선수 이름",
            "TEAM_ABBREVIATION": "팀",
            "GP": "경기 수",
            "PTS": "득점",
            "REB": "리바운드",
            "AST": "어시스트",
            "STL": "스틸",
            "BLK": "블락"
        })
        result = result.reset_index(drop=True)

        return result

    except Exception as e:
        return f"Error fetching player stats: {str(e)}"

print(get_season_player_stats("2024-25", top_n=5))

