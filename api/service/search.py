from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo

def name_to_info(fullname):
    # 모든 선수 목록 가져오기
    player_list = players.get_players()
    
    # 정확히 이름이 일치하는 선수 찾기
    matching = [p for p in player_list if p['full_name'].lower() == fullname.lower()]
    
    if not matching:
        return f"No player found with full name: {fullname}", None, None

    player = matching[0]
    player_id = player['id']

    # 선수 기본 정보 가져오기
    info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
    data = info.get_dict()

    # 헤더 및 원하는 정보 추출
    headers = ["성", "이름", "생년월일", "키", "몸무게", "등번호", "포지션", "팀"]
    raw = data["resultSets"][0]["rowSet"][0]
    
    rowSet = [
        raw[1],   # First Name
        raw[2],   # Last Name
        raw[7],   # Birth Date
        raw[11],  # Height
        raw[12],  # Weight
        raw[14],  # Jersey
        raw[15],  # Position
        raw[19]   # Team Name
    ]

    # 선수 사진 URL
    image_url = f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player_id}.png"

    return headers, rowSet, image_url, player_id


def get_full_name(name):
    # 모든 선수 정보 가져오기
    all_players = players.get_players()
    
    # 이름에 부분 문자열이 포함된 선수 필터링 (대소문자 무시)
    matching_players = [p for p in all_players if name.lower() in p['full_name'].lower()]
    
    if not matching_players:
        return f"No player found with partial name: {name}"
    return matching_players[0]['full_name']




