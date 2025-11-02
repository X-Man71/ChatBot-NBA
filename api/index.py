from turtle import title
from flask import Flask, request, render_template, redirect, jsonify, send_from_directory, url_for, abort, session
from service.utils import load_posts, save_posts
from nba_api.stats.endpoints import leaguedashplayerstats
from nba_api.stats.endpoints import leaguegamefinder
from service.kakaologin import get_user_info_from_kakao, kakao_login
from nba_api.stats.static import players
import pandas as pd
import requests, random
import json
import service.player_rank as player_rank
import service.search as search
import service.team_name as team_name
import service.teamrank as teamrank
from const.team_constant import TEAM_NAME
import service.players as players
import feedparser
import time
import threading
app = Flask(__name__)
app.secret_key = "whatthehell" #SESSION을 사용하려면 KEY를 작성해줘야한다.


"""
게임 데이터
"""


games_data = [{'SEASON_ID': '22024', 'TEAM_ID': 1610612741, 'TEAM_ABBREVIATION': 'CHI', 'TEAM_NAME': 'Chicago Bulls', 'GAME_ID': '0022401191', 'GAME_DATE': '2025-04-13', 'MATCHUP': 'CHI @ PHI', 'WL': 'W', 'MIN': 240, 'PTS': 122, 'FGM': 47, 'FGA': 103, 'FG_PCT': 0.456, 'FG3M': 13, 'FG3A': 40, 'FG3_PCT': 0.325, 'FTM': 15, 'FTA': 20, 'FT_PCT': 0.75, 'OREB': 15, 'DREB': 44, 'REB': 59, 'AST': 29, 'STL': 10, 'BLK': 4, 'TOV': 12, 'PF': 17, 'PLUS_MINUS': 20.0}, 
              {'SEASON_ID': '22024', 'TEAM_ID': 1610612753, 'TEAM_ABBREVIATION': 'ORL', 'TEAM_NAME': 'Orlando Magic', 'GAME_ID': '0022401186', 'GAME_DATE': '2025-04-13', 'MATCHUP': 'ORL @ ATL', 'WL': 'L', 'MIN': 240, 'PTS': 105, 'FGM': 40, 'FGA': 88, 'FG_PCT': 0.455, 'FG3M': 15, 'FG3A': 35, 'FG3_PCT': 0.429, 'FTM': 10, 'FTA': 15, 'FT_PCT': 0.667, 'OREB': 12, 'DREB': 31, 'REB': 43, 'AST': 25, 'STL': 11, 'BLK': 5, 'TOV': 14, 'PF': 8, 'PLUS_MINUS': -12.0},
              {'SEASON_ID': '22024', 'TEAM_ID': 1610612742, 'TEAM_ABBREVIATION': 'DAL', 'TEAM_NAME': 'Dallas Mavericks', 'GAME_ID': '0022401194', 'GAME_DATE': '2025-04-13', 'MATCHUP': 'DAL @ MEM', 'WL': 'L', 'MIN': 240, 'PTS': 97, 'FGM': 38, 'FGA': 87, 'FG_PCT': 0.437, 'FG3M': 5, 'FG3A': 28, 'FG3_PCT': 0.179, 'FTM': 16, 'FTA': 22, 'FT_PCT': 0.727, 'OREB': 10, 'DREB': 28, 'REB': 38, 'AST': 20, 'STL': 6, 'BLK': 3, 'TOV': 18, 'PF': 13, 'PLUS_MINUS': -35.0}, 
              {'SEASON_ID': '22024', 'TEAM_ID': 1610612739, 'TEAM_ABBREVIATION': 'CLE', 'TEAM_NAME': 'Cleveland Cavaliers', 'GAME_ID': '0022401189', 'GAME_DATE': '2025-04-13', 'MATCHUP': 'CLE vs. IND', 'WL': 'L', 'MIN': 292, 'PTS': 118, 'FGM': 44, 'FGA': 115, 'FG_PCT': 0.383, 'FG3M': 18, 'FG3A': 60, 'FG3_PCT': 0.3, 'FTM': 12, 'FTA': 22, 'FT_PCT': 0.545, 'OREB': 18, 'DREB': 47, 'REB': 65, 'AST': 21, 'STL': 6, 'BLK': 9, 'TOV': 21, 'PF': 23, 'PLUS_MINUS': -8.0},
              {'SEASON_ID': '22024', 'TEAM_ID': 1610612745,'TEAM_ABBREVIATION': 'HOU', 'TEAM_NAME': 'Houston Rockets', 'GAME_ID': '0022401193', 'GAME_DATE': '2025-04-13', 'MATCHUP': 'HOU vs. DEN', 'WL': 'L', 'MIN': 239, 'PTS': 111, 'FGM': 45, 'FGA': 100, 'FG_PCT': 0.45, 'FG3M': 12, 'FG3A': 34, 'FG3_PCT': 0.353, 'FTM': 9, 'FTA': 14, 'FT_PCT': 0.643, 'OREB': 16, 'DREB': 29, 'REB': 45, 'AST': 32, 'STL': 5, 'BLK': 4, 'TOV': 10, 'PF': 24, 'PLUS_MINUS': -15.0}, 
              {'SEASON_ID': '22024', 'TEAM_ID': 1610612747, 'TEAM_ABBREVIATION': 'LAL', 'TEAM_NAME': 'Los Angeles Lakers', 'GAME_ID': '0022401199', 'GAME_DATE': '2025-04-13', 'MATCHUP': 'LAL @ POR', 'WL': 'L', 'MIN': 239, 'PTS': 81, 'FGM': 31, 'FGA': 80, 'FG_PCT': 0.388, 'FG3M': 9, 'FG3A': 28, 'FG3_PCT': 0.321, 'FTM': 10, 'FTA': 14, 'FT_PCT': 0.714, 'OREB': 13, 'DREB': 29, 'REB': 42, 'AST': 21, 'STL': 9, 'BLK': 11, 'TOV': 20, 'PF': 21, 'PLUS_MINUS': -28.0}, 
              {'SEASON_ID': '22024', 'TEAM_ID': 1610612746, 'TEAM_ABBREVIATION': 'LAC', 'TEAM_NAME': 'LA Clippers', 'GAME_ID': '0022401198', 'GAME_DATE': '2025-04-13', 'MATCHUP': 'LAC @ GSW', 'WL': 'W', 'MIN': 265, 'PTS': 124, 'FGM': 48, 'FGA': 86, 'FG_PCT': 0.558, 'FG3M': 14, 'FG3A': 30, 'FG3_PCT': 0.467, 'FTM': 14, 'FTA': 18, 'FT_PCT': 0.778, 'OREB': 9, 'DREB': 33, 'REB': 42, 'AST': 28, 'STL': 11, 'BLK': 3, 'TOV': 16, 'PF': 21, 'PLUS_MINUS': 5.0}, 
              {'SEASON_ID': '22024', 'TEAM_ID': 1610612744, 'TEAM_ABBREVIATION': 'GSW', 'TEAM_NAME': 'Golden State Warriors', 'GAME_ID': '0022401198', 'GAME_DATE': '2025-04-13', 'MATCHUP': 'GSW vs. LAC', 'WL': 'L', 'MIN': 265, 'PTS': 119, 'FGM': 43, 'FGA': 79, 'FG_PCT': 0.544, 'FG3M': 15, 'FG3A': 33, 'FG3_PCT': 0.455, 'FTM': 18, 'FTA': 23, 'FT_PCT': 0.783, 'OREB': 3, 'DREB': 22, 'REB': 25, 'AST': 31, 'STL': 11, 'BLK': 6, 'TOV': 15, 'PF': 20, 'PLUS_MINUS': -5.0}, 
              {'SEASON_ID': '22024', 'TEAM_ID': 1610612763, 'TEAM_ABBREVIATION': 'MEM', 'TEAM_NAME': 'Memphis Grizzlies', 'GAME_ID': '0022401194', 'GAME_DATE': '2025-04-13', 'MATCHUP': 'MEM vs. DAL', 'WL': 'W', 'MIN': 239, 'PTS': 132, 'FGM': 52, 'FGA': 104, 'FG_PCT': 0.5, 'FG3M': 15, 'FG3A': 40, 'FG3_PCT': 0.375, 'FTM': 13, 'FTA': 15, 'FT_PCT': 0.867, 'OREB': 19, 'DREB': 34, 'REB': 53, 'AST': 31, 'STL': 13, 'BLK': 7, 'TOV': 11, 'PF': 15, 'PLUS_MINUS': 35.0}, 
              {'SEASON_ID': '22024', 'TEAM_ID': 1610612766, 'TEAM_ABBREVIATION': 'CHA', 'TEAM_NAME': 'Charlotte Hornets', 'GAME_ID': '0022401187', 'GAME_DATE': '2025-04-13', 'MATCHUP': 'CHA @ BOS', 'WL': 'L', 'MIN': 240, 'PTS': 86, 'FGM': 32, 'FGA': 85, 'FG_PCT': 0.376, 'FG3M': 11, 'FG3A': 39, 'FG3_PCT': 0.282, 'FTM': 11, 'FTA': 18, 'FT_PCT': 0.611, 'OREB': 18, 'DREB': 33, 'REB': 51, 'AST': 23, 'STL': 10, 'BLK': 4, 'TOV': 17, 'PF': 16, 'PLUS_MINUS': -7.0}, 
              {'SEASON_ID': '22024', 'TEAM_ID': 1610612740, 'TEAM_ABBREVIATION': 'NOP', 'TEAM_NAME': 'New Orleans Pelicans', 'GAME_ID': '0022401196', 'GAME_DATE': '2025-04-13', 'MATCHUP': 'NOP vs. OKC', 'WL': 'L', 'MIN': 240, 'PTS': 100, 'FGM': 35, 'FGA': 91, 'FG_PCT': 0.385, 'FG3M': 7, 'FG3A': 38, 'FG3_PCT': 0.184, 'FTM': 23, 'FTA': 30, 'FT_PCT': 0.767, 'OREB': 11, 'DREB': 36, 'REB': 47, 'AST': 22, 'STL': 6, 'BLK': 4, 'TOV': 12, 'PF': 19, 'PLUS_MINUS': -15.0}, 
              {'SEASON_ID': '22024', 'TEAM_ID': 1610612756, 'TEAM_ABBREVIATION': 'PHX', 'TEAM_NAME': 'Phoenix Suns', 'GAME_ID': '0022401200', 'GAME_DATE': '2025-04-13', 'MATCHUP': 'PHX @ SAC', 'WL': 'L', 'MIN': 241, 'PTS': 98, 'FGM': 40, 'FGA': 84, 'FG_PCT': 0.476, 'FG3M': 15, 'FG3A': 44, 'FG3_PCT': 0.341, 'FTM': 3, 'FTA': 6, 'FT_PCT': 0.5, 'OREB': 9, 'DREB': 28, 'REB': 37, 'AST': 28, 'STL': 6, 'BLK': 1, 'TOV': 11, 'PF': 9, 'PLUS_MINUS': -11.0}, 
              {'SEASON_ID': '22024', 'TEAM_ID': 1610612751, 'TEAM_ABBREVIATION': 'BKN', 'TEAM_NAME': 'Brooklyn Nets', 'GAME_ID': '0022401188', 'GAME_DATE': '2025-04-13', 'MATCHUP': 'BKN vs. NYK', 'WL': 'L', 'MIN': 239, 'PTS': 105, 'FGM': 38, 'FGA': 74, 'FG_PCT': 0.514, 'FG3M': 12, 'FG3A': 35, 'FG3_PCT': 0.343, 'FTM': 17, 'FTA': 25, 'FT_PCT': 0.68, 'OREB': 6, 'DREB': 36, 'REB': 42, 'AST': 21, 'STL': 4, 'BLK': 2, 'TOV': 18, 'PF': 24, 'PLUS_MINUS': -8.0}, 
              {'SEASON_ID': '22024', 'TEAM_ID': 1610612765, 'TEAM_ABBREVIATION': 'DET', 'TEAM_NAME': 'Detroit Pistons', 'GAME_ID': '0022401192', 'GAME_DATE': '2025-04-13', 'MATCHUP': 'DET @ MIL', 'WL': 'L', 'MIN': 264, 'PTS': 133, 'FGM': 51, 'FGA': 107, 'FG_PCT': 0.477, 'FG3M': 22, 'FG3A': 59, 'FG3_PCT': 0.373, 'FTM': 9, 'FTA': 14, 'FT_PCT': 0.643, 'OREB': 14, 'DREB': 28, 'REB': 42, 'AST': 35, 'STL': 9, 'BLK': 3, 'TOV': 13, 'PF': 19, 'PLUS_MINUS': -7.0}, 
              {'SEASON_ID': '22024', 'TEAM_ID': 1610612737, 'TEAM_ABBREVIATION': 'ATL', 'TEAM_NAME': 'Atlanta Hawks', 'GAME_ID': '0022401186', 'GAME_DATE': '2025-04-13', 'MATCHUP': 'ATL vs. ORL', 'WL': 'W', 'MIN': 241, 'PTS': 117, 'FGM': 47, 'FGA': 88, 'FG_PCT': 0.534, 'FG3M': 17, 'FG3A': 40, 'FG3_PCT': 0.425, 'FTM': 6, 'FTA': 10, 'FT_PCT': 0.6, 'OREB': 9, 'DREB': 35, 'REB': 44, 'AST': 32, 'STL': 8, 'BLK': 2, 'TOV': 15, 'PF': 15, 'PLUS_MINUS': 12.0}, 
              {'SEASON_ID': '22024', 'TEAM_ID': 1610612762, 'TEAM_ABBREVIATION': 'UTA', 'TEAM_NAME': 'Utah Jazz', 'GAME_ID': '0022401195', 'GAME_DATE': '2025-04-13', 'MATCHUP': 'UTA @ MIN', 'WL': 'L', 'MIN': 241, 'PTS': 105, 'FGM': 40, 'FGA': 89, 'FG_PCT': 0.449, 'FG3M': 16, 'FG3A': 42, 'FG3_PCT': 0.381, 'FTM': 9, 'FTA': 11, 'FT_PCT': 0.818, 'OREB': 9, 'DREB': 31, 'REB': 40, 'AST': 24, 'STL': 6, 'BLK': 5, 'TOV': 13, 'PF': 15, 'PLUS_MINUS': -11.0}, 
              {'SEASON_ID': '22024', 'TEAM_ID': 1610612761, 'TEAM_ABBREVIATION': 'TOR', 'TEAM_NAME': 'Toronto Raptors', 'GAME_ID': '0022401197', 'GAME_DATE': '2025-04-13', 'MATCHUP': 'TOR @ SAS', 'WL': 'L', 'MIN': 240, 'PTS': 118, 'FGM': 46, 'FGA': 97, 'FG_PCT': 0.474, 'FG3M': 14, 'FG3A': 39, 'FG3_PCT': 0.359, 'FTM': 12, 'FTA': 16, 'FT_PCT': 0.75, 'OREB': 12, 'DREB': 30, 'REB': 42, 'AST': 32, 'STL': 8, 'BLK': 1, 'TOV': 13, 'PF': 23, 'PLUS_MINUS': -7.0}, 
              {'SEASON_ID': '22024', 'TEAM_ID': 1610612755, 'TEAM_ABBREVIATION': 'PHI', 'TEAM_NAME': 'Philadelphia 76ers', 'GAME_ID': '0022401191', 'GAME_DATE': '2025-04-13', 'MATCHUP': 'PHI vs. CHI', 'WL': 'L', 'MIN': 240, 'PTS': 102, 'FGM': 36, 'FGA': 94, 'FG_PCT': 0.383, 'FG3M': 12, 'FG3A': 44, 'FG3_PCT': 0.273, 'FTM': 18, 'FTA': 21, 'FT_PCT': 0.857, 'OREB': 10, 'DREB': 38, 'REB': 48, 'AST': 20, 'STL': 7, 'BLK': 6, 'TOV': 14, 'PF': 15, 'PLUS_MINUS': -20.0}, 
              {'SEASON_ID': '22024', 'TEAM_ID': 1610612749, 'TEAM_ABBREVIATION': 'MIL', 'TEAM_NAME': 'Milwaukee Bucks', 'GAME_ID': '0022401192', 'GAME_DATE': '2025-04-13', 'MATCHUP': 'MIL vs. DET', 'WL': 'W', 'MIN': 265, 'PTS': 140, 'FGM': 50, 'FGA': 86, 'FG_PCT': 0.581, 'FG3M': 23, 'FG3A': 44, 'FG3_PCT': 0.523, 'FTM': 17, 'FTA': 22, 'FT_PCT': 0.773, 'OREB': 6, 'DREB': 32, 'REB': 38, 'AST': 30, 'STL': 5, 'BLK': 7, 'TOV': 20, 'PF': 17, 'PLUS_MINUS': 7.0}, 
              {'SEASON_ID': '22024', 'TEAM_ID': 1610612759, 'TEAM_ABBREVIATION': 'SAS', 'TEAM_NAME': 'San Antonio Spurs', 'GAME_ID': '0022401197', 'GAME_DATE': '2025-04-13', 'MATCHUP': 'SAS vs. TOR', 'WL': 'W', 'MIN': 240, 'PTS': 125, 'FGM': 43, 'FGA': 84, 'FG_PCT': 0.512, 'FG3M': 11, 'FG3A': 32, 'FG3_PCT': 0.344, 'FTM': 28, 'FTA': 32, 'FT_PCT': 0.875, 'OREB': 9, 'DREB': 41, 'REB': 50, 'AST': 22, 'STL': 11, 'BLK': 2, 'TOV': 12, 'PF': 13, 'PLUS_MINUS': 7.0}]

# 상수 선언은 함수 최상단으로
NEWS_API_KEY = 'd5ef6f58589b459ead2200a67f4cd344'
MAX_PAGE = 101
PAGE_SIZE = 80
BALL_API = "https://www.balldontlie.io/api/v1"

"""
아래는 KAKAO API 에 대한 함수들입니다.
"""

#카카오챗봇 팀 검색 API                   
@app.route("/team", methods=["POST"])  
def search_team():
    json_data = request.get_json(force=True)
    user_request = json_data['userRequest']
    utterance = user_request['utterance']
    lst = utterance.split()
    name = lst[-1]
    teamname = team_name.get_team_info(name)
    info = teamname[0]
    imageUrl = teamname[1]

    response = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": info['fullName'],
                        "description": (
                            f"약어: {info['abb']}\n"
                            f"도시: {info['city']} / 닉네임: {info['nickname']}\n"
                         ),
                        "thumbnail": {
                            "imageUrl": imageUrl
                        },
                        "buttons": [
                            {
                                "label": "NBA 프로필 보기",
                                "action": "webLink"
                            }
                        ]
                    }
                }
            ]
        }
        }
    return jsonify(response)

#선수 검색
@app.route("/player", methods=["POST"])
def search_player():
    try:
        json_data = request.get_json(force=True)
        user_request = json_data['userRequest']
        utterance = user_request['utterance']
        lst = utterance.split()
        name = lst[-1]
        full_name = search.get_full_name(name)
        a = search.name_to_info(full_name)
        info = a[1]
        imageUrl = a[2]

        response = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": info[0] + " " + info[1],  # 성 + 이름
                        "description": (
                            f"생년월일: {info[2]}\n"
                            f"키: {info[3]} / 몸무게: {info[4]}\n"
                            f"등번호: {info[5]} | 포지션: {info[6]}\n"
                            f"팀: {info[7]}"
                         ),
                        "thumbnail": {
                            "imageUrl": imageUrl
                        },
                        "buttons": [
                            {
                                "label": "NBA 프로필 보기",
                                "action": "webLink"
                            }
                        ]
                    }
                }
            ]
        }
        }
        return jsonify(response)
    except Exception as e:
        print("exception")
        json_data = {}
    return jsonify({})


# 선수 랭킹
@app.route('/rank', methods=["POST","GET"])
def real_rank():
    ranking = player_rank.get_season_player_rankings("2024-25", top_n=10, stat="PTS")

    items = []
    for player in ranking:
        item = {
            "title": player["선수 이름"],
            "description": (
                f"팀: {player['팀']}\n"
                f"경기수: {player['경기수']}\n"
                f"PTS: {player['PTS']}"
            ),
            "imageUrl": player["image_url"],  # 여기서 바로 사용
            "link": {
                "web": "https://www.nba.com/players"  # 필요시 개별 링크로 확장 가능
            }
        }
        items.append(item)

    response = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "listCard": {
                        "header": {
                            "title": f"PTS Top {len(ranking)} 선수 랭킹"
                        },
                        "items": items
                    }
                }
            ]
        }
    }
    return jsonify(response)

# 팀 랭킹
@app.route('/team_rank', methods=["POST","GET"])
def search_rank():
    t_ranking = teamrank.get_season_team_rankings(2024-25, top_n=10)
    items = [] 
    for team in t_ranking:
        image_url = teamrank.get_team_logo(team["팀 이름"])
        item = {
            "title": team["팀 이름"],
            "description": (
                f"승: {team['승']}\n"
                f"패: {team['패']}\n"
                f"승률: {team['승률']}"
            ),
            "imageUrl": image_url,  # 여기서 바로 사용
            "link": {
                "web": "https://www.nba.com/teams"  # 필요시 개별 링크로 확장 가능
            }
        }
        items.append(item)

    response = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "listCard": {
                        "header": {
                            "title": f"Top {len(t_ranking)} 팀 랭킹"
                        },
                        "items": items
                    }
                }
            ]
        }
    }

    return jsonify(response)

# NBA 뉴스(카카오ver)
@app.route("/news", methods=["POST"])
def news():
    try:
        user_request = request.get_json()
        utterance = user_request['userRequest']['utterance'].strip()

        if "뉴스" in utterance:  # "뉴스"라는 단어가 포함된 경우에만 뉴스 제공
            news = get_basketball_news()


            if news:
                response = {
                    "version": "2.0",
                    "template": {
                        "outputs": [
                            {
                                "listCard": {
                                    "header": {
                                        "title": news["title"]
                                    },
                                    "items": [
                                        {
                                            "title": news["title"],
                                            "imageUrl": news["image"] if news["image"] else "",  # Image URL
                                            "link": {
                                                "web": news["link"]
                                            }
                                        }
                                    ],
                                    "buttons": [
                                        {
                                            "action": "webLink",
                                            "label": "본문 보기",
                                            "webLinkUrl": news["link"]
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                }

                return jsonify(response)
            else:
                return jsonify({
                    "version": "2.0",
                    "template": {
                        "outputs": [
                            {
                                "simpleText": {
                                    "text": "NBA 뉴스를 찾을 수 없습니다."
                                }
                            }
                        ]
                    }
                })
        else:
            return jsonify({
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "NBA 뉴스와 관련된 요청이 없습니다."
                            }
                        }
                    ]
                }
            })

    except Exception as e:
        print(f"Error handling request: {e}")
        return jsonify({
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "요청을 처리하는 중 오류가 발생했습니다."
                        }
                    }
                ]
            }
        })

"""
웹페이지 라우트함수
"""

@app.route("/")
def home():
    if "kakao_token" in session: #세션안에 카카오토큰이 있으면...
        return render_template("name.html", token=True)
    else:
        return render_template("name.html")


@app.route("/player_list", methods=['GET', 'POST'])
def player_list():

    # 기본 페이지 번호, GET/POST 상관없이 사용하기 위해 여기서 처리
    page = request.args.get('page', '1')
    try:
        current_page = int(page)
    except ValueError:
        current_page = 1

    if request.method == 'POST': #검색했을 때
        user_input = request.form.get('keyword', '').strip()
        if user_input:
            info = players.get_players_by_name(user_input)
            # 검색 결과가 1명이라면 info는 dict, 여러명이라면 리스트 가정
            if isinstance(info, dict):
                return render_template("player_list.html", info=info, current_page=1, max_page=1)
            elif isinstance(info, list):
                # 여러명 검색 결과가 있다면 페이지네이션 없이 한 페이지에 다 보여주는 예시
                return render_template("player_list.html", player_lst=info, current_page=1, max_page=1)
            else:#검색 결과가 없을 때
                return render_template("player_list.html", player_lst=[], current_page=1, max_page=1)
        else:
            # 빈 검색어 처리 (전체 선수 목록 보여주기 등)
            pass  # 아래 GET 처리와 동일하게 처리하겠습니다

    # GET 요청 처리 및 POST에서 빈 검색어 넘어왔을 때도 여기서 처리
    player_lst = players.get_all_players(current_page)
    # players.get_all_players()가 페이지 단위로 선수 리스트 반환한다고 가정

    return render_template("player_list.html",
                           player_lst=player_lst,
                           current_page=current_page,
                           max_page=MAX_PAGE)


@app.route("/special", methods=['GET'])
def special():
    return render_template('special.html')



def get_recent_game_from_data():
    """주어진 경기 기록에서 무작위 경기 선택"""
    if not games_data:
        return None
    return random.choice(games_data)

@app.route("/ran", methods=["GET", "POST"])
def ran():
    if request.method == "POST":
        # 사용자 답안 확인
        answer = request.form.get("answer", "").strip().upper()
        team_abb = request.form.get("TEAM_ABBREVIATION", "").strip().upper()

        is_correct = (answer == team_abb)

        message = (
            f"✅ 정답입니다! ({team_abb})"
            if is_correct
            else f"❌ 오답! 정답은 {team_abb} 입니다."
        )
        return render_template("result.html", message=message)

    # GET 요청 → 퀴즈 생성
    game = get_recent_game_from_data()
    if not game:  # dict 비었을 때
        return "<h3>⚠️ 경기 기록이 없습니다.</h3>"

    # dict에서 정보 추출
    winning_team = game.get('TEAM_ABBREVIATION', '알 수 없음')
    matchup = game.get('MATCHUP', '정보 없음')
    question = f"{matchup} 경기에서 승리한 팀은 어디일까요?"

    return render_template(
        'ran.html',
        question=question,
        team_name=winning_team   # 정답
    )


@app.route('/get_nba_news')
def get_nba_news():
    try:
        resp = requests.get('https://site.api.espn.com/apis/site/v2/sports/basketball/nba/news')
        resp.raise_for_status()
        data = resp.json()

        # 뉴스 항목 추출 (예: headlines)
        articles = data.get('articles', []) or data.get('headlines', [])
        result = []
        for item in articles:
            result.append({
                "title": item.get("headline") or item.get("title"),
                "summary": item.get("description") or "",
                "url": item.get("links", {}).get("web", {}).get("href") or item.get("links", {}).get("mobile", {}).get("href")
            })
        return jsonify(result)

    except Exception as e:
        print("ESPN 뉴스 API 오류:", e)
        return jsonify([]), 500

def get_basketball_news():
    try:
        rss_url = "https://news.google.com/rss/search?q=NBA&hl=ko&gl=KR&ceid=KR:ko"
        feed = feedparser.parse(rss_url)

        if not feed.entries:
            return None

        top_news = feed.entries[0]  # 가장 최신 뉴스
        return {
            "title": top_news.title,
            "link": top_news.link,
            "image": top_news.media_thumbnail[0]['url'] if 'media_thumbnail' in top_news else None
        }
    except Exception as e:
        print(f"Error fetching NBA news: {e}")
        return None

# NBA 경기 데이터 가져오는 함수
def get_nba_game_data():
    game_finder = leaguegamefinder.LeagueGameFinder()
    games_df = game_finder.get_data_frames()[0]  # 첫 번째 DataFrame을 사용
    return games_df  # DataFrame 반환

# 데이터에 페이지네이션을 적용하는 함수
def paginate_data(df, page, page_size):
    start_row = (page - 1) * page_size
    end_row = start_row + page_size
    paginated_df = df.iloc[start_row:end_row]
    return paginated_df

#경기 기록
@app.route('/game')
def game():
    page = request.args.get('page', default=1, type=int)  # 현재 페이지 (디폴트는 1)
    games_df = get_nba_game_data()  # NBA 경기 데이터 가져오기

    # 페이지네이션 적용
    paginated_games = paginate_data(games_df, page, PAGE_SIZE)
    
    # 데이터 프레임을 리스트로 변환
    games_data = paginated_games.to_dict(orient='records')
    
    # 전체 페이지 수 계산
    total_pages = (len(games_df) // PAGE_SIZE) + (1 if len(games_df) % PAGE_SIZE > 0 else 0)

    return render_template('game.html', games=games_data, page=page, total_pages=total_pages)


#카카오 로그인 페이지 보여주는 Route 함수 
@app.route('/login', methods = ['GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/')
    
#카카오 로그인 콜백 함수
@app.route("/callback", methods=['GET'])
def callback():
    code = request.args.get('code') #주소창에 있는 code의 값을 뽑아내기
    token = kakao_login(code) #KAKAO 에서 발급해준 ACCESS_TOKEN을 token변수에 저장. -> 로그인 완료
    if token: #로그인이 완료 되었다면...
        session['kakao_token'] = token #세션(카카오토큰)에 token을 저장
    return redirect("/")#메인 페이지로

latest_news = {}

#뉴스 갱신 하루마다 실행
def update_news():
    """하루마다 실행할 뉴스 업데이트 함수"""
    global latest_news
    try:
        rss_url = "https://news.google.com/rss/search?q=NBA&hl=ko&gl=KR&ceid=KR:ko"
        feed = feedparser.parse(rss_url)
        if feed.entries:
            top_news = feed.entries[0]
            latest_news = {
                "title": top_news.title,
                "link": top_news.link,
                "image": top_news.media_thumbnail[0]['url'] if 'media_thumbnail' in top_news else None
            }
            print("[뉴스 업데이트 완료] ", latest_news["title"])
        else:
            print("[뉴스 업데이트 실패] 뉴스 항목이 없습니다.")
    except Exception as e:
        print("[뉴스 업데이트 오류]", e)

def periodic_task():
    while True:
        update_news()
        time.sleep(3600)  # 3600초 = 1시간 , 86400초 = 24시간

def start_periodic_task():
    thread = threading.Thread(target=periodic_task)
    thread.daemon = True
    thread.start()

@app.route("/news_latest")
def news_latest():
    """저장된 최신 뉴스 반환"""
    if latest_news:
        return jsonify(latest_news)
    else:
        return jsonify({"message": "뉴스가 아직 업데이트되지 않았습니다."})


"""
커뮤니티 기능
Create, Read, Update, Delete 구현
"""

# 게시판 기능
community_posts = load_posts()

@app.route('/community')
def community():
    try:
        return render_template('community.html', posts=community_posts)
    except Exception as e:
        print(f"[ERROR] 커뮤니티 페이지 렌더링 실패: {e}")
        return "오류가 발생했습니다. 잠시 후 다시 시도해주세요.", 500


@app.route('/community/write', methods=['GET', 'POST'])
def write_post():
    author = "익명"
    try:
        if "kakao_token" in session:
            kakao_token = session["kakao_token"]
            user_info = get_user_info_from_kakao(kakao_token)
            print(user_info)
            if user_info:
                kakao_account = user_info.get('kakao_account', {})
                profile = kakao_account.get('profile', {})
                email = kakao_account.get('email', '이메일 없음')
                nickname = profile.get('nickname', '익명')
                author = nickname
                print(f"User info: email={email}, nickname={nickname}")

        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            post = {
                "title": title,
                "content": content,
                "author": author,
                "comments": []
            }
            community_posts.append(post)
            save_posts(community_posts)
            return redirect(url_for('community'))

        return render_template('write_post.html', author=author)

    except Exception as e:
        print(f"[ERROR] 게시글 작성 중 오류: {e}")
        return "게시글 작성 중 오류가 발생했습니다.", 500


@app.route('/community/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    try:
        if not (0 <= post_id < len(community_posts)):
            abort(404)
        post = community_posts[post_id]

        if request.method == 'POST':
            new_title = request.form['title']
            new_content = request.form['content']
            post['title'] = new_title
            post['content'] = new_content
            save_posts(community_posts)
            return redirect(url_for('community'))

        return render_template('edit_post.html', post=post, post_id=post_id)

    except Exception as e:
        print(f"[ERROR] 게시글 수정 중 오류: {e}")
        return "게시글 수정 중 문제가 발생했습니다.", 500


@app.route('/community/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    try:
        if not (0 <= post_id < len(community_posts)):
            abort(404)
        community_posts.pop(post_id)
        save_posts(community_posts)
        return redirect(url_for('community'))
    except Exception as e:
        print(f"[ERROR] 게시글 삭제 중 오류: {e}")
        return "게시글 삭제 중 문제가 발생했습니다.", 500


@app.route('/community/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    try:
        if not (0 <= post_id < len(community_posts)):
            abort(404)
        comment = request.form['comment']
        community_posts[post_id]["comments"].append(comment)
        save_posts(community_posts)
        return redirect(url_for('community'))
    except Exception as e:
        print(f"[ERROR] 댓글 추가 중 오류: {e}")
        return "댓글 추가 중 오류가 발생했습니다.", 500


@app.route('/community/<int:post_id>/comment/<int:comment_id>/delete', methods=['POST'])
def delete_comment(post_id, comment_id):
    try:
        if not (0 <= post_id < len(community_posts)):
            abort(404)
        comments = community_posts[post_id]["comments"]
        if not (0 <= comment_id < len(comments)):
            abort(404)
        comments.pop(comment_id)
        save_posts(community_posts)
        return redirect(url_for('community'))
    except Exception as e:
        print(f"[ERROR] 댓글 삭제 중 오류: {e}")
        return "댓글 삭제 중 오류가 발생했습니다.", 500


if __name__ == "__main__":
    start_periodic_task()

    app.run(host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'), debug=True)
