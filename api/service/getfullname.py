from nba_api.stats.static import players

def get_full_name(name):
    # 모든 선수 정보 가져오기
    all_players = players.get_players()
    
    # 이름에 부분 문자열이 포함된 선수 필터링 (대소문자 무시)
    matching_players = [p for p in all_players if name.lower() in p['full_name'].lower()]
    
    if not matching_players:
        return f"No player found with partial name: {name}"
    
    # 첫 번째 매칭되는 선수의 풀네임만 반환
    return matching_players[0]['full_name']

