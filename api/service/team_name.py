from nba_api.stats.static import teams

def get_team_info(teamname):
    # 모든 NBA 팀 정보 가져오기
    all_teams = teams.get_teams()
    
    # 입력한 이름이 포함된 팀 검색 (대소문자 무시)
    matching_teams = [team for team in all_teams if teamname.lower() in team['full_name'].lower()]
    
    if not matching_teams:
        return f"No team found with partial name: {teamname}", None
    
    # 첫 번째 일치하는 팀 선택
    team = matching_teams[0]
    
    # 팀 정보
    team_id = team['id']
    full_name = team['full_name']
    nickname = team['nickname']
    city = team['city']
    abbreviation = team['abbreviation']

    # NBA 팀 로고 이미지 URL (공식 CDN 사용)
    image_url = f"https://cdn.nba.com/logos/nba/{team_id}/global/L/logo.svg"

    # 결과 반환
    info = {
        "fullName": full_name,
        "abb": abbreviation,
        "city": city,
        "nickname": nickname
    }

    return info, image_url
