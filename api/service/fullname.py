from nba_api.stats.static import teams

def get_team_fullname(partial_name: str):
    """
    팀 이름 일부를 입력하면 일치하는 팀의 전체 이름을 반환합니다.
    
    Parameters:
    - partial_name (str): 팀 이름의 일부 (예: 'lakers', 'war')
    
    Returns:
    - str: 일치하는 팀의 전체 이름 (예: 'Los Angeles Lakers')
    """
    all_teams = teams.get_teams()

    # 대소문자 구분 없이 검색
    matches = [team for team in all_teams if partial_name.lower() in team['full_name'].lower()]
    
    if not matches:
        return f"No team found with partial name: {partial_name}"
    
    # 첫 번째 일치 항목 반환
    return matches[0]['full_name']


def get_team_info(teamname):
    # 모든 NBA 팀 정보 가져오기
    from nba_api.stats.static import teams
    all_teams = teams.get_teams()
    
    # 입력한 이름이 포함된 팀 검색 (대소문자 무시)
    matching_teams = [team for team in all_teams if teamname.lower() in team['full_name'].lower()]
    
    if not matching_teams:
        return f"No team found with partial name: {teamname}", None
    
    # 첫 번째 일치하는 팀 선택
    teams = matching_teams[0]
    
    # 팀 정보
    team_id = teams['id']
    full_name = teams['full_name']
    nickname = teams['nickname']
    city = teams['city']
    abbreviation = teams['abbreviation']


    # 결과 반환
    info2 = {
        "팀 id":  team_id,
        "팀 전체 이름": full_name,
        "약어": abbreviation,
        "도시": city,
        "닉네임": nickname,
    }

    return info2

print(get_team_info('Lakers'))
