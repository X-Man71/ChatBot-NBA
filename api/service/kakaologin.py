import requests
import json

def kakao_login(code):
    url = "https://kauth.kakao.com/oauth/token"
    headers={
        "Content-Type":"application/x-www-form-urlencoded;charset=utf-8"
    }
    body={
        "grant_type":"authorization_code",
        "client_id":"4727b876fbf37e21bd488df5bc9f62d9",
        "redirect_uri":"http://127.0.0.1:5000/callback",
        "code": code,
        "client_secret":"aQAUnGe0e6P0uPrT06otJN4YwBcZCts5"
    }
    
    try:
        response = requests.post(url=url,data=body,headers=headers)
        response = response.json()
        access_token = response['access_token']
        print(access_token)
    except Exception as e:
        print("some issues..")
        print(e)
    try:
        bearer_token = "Bearer "+ access_token
        url = "https://kapi.kakao.com/v2/user/me"
        headers = {
            "Authorization": bearer_token,
            "Content-Type":"application/x-www-form-urlencoded;charset=utf-8"
        }
        response = requests.get(url=url, headers=headers)
        print(response.status_code)
        print(response.text)
    except Exception as e:
        print("some issues..")
        print(e)
        return None
    print(response.json())
    user_json = response.json()
    print(user_json)
        # 이메일과 닉네임 추출 (존재 여부 확인 필요)
    kakao_account = user_json.get('kakao_account', {})
    profile = kakao_account.get('profile', {})
    print(kakao_account)
    print(profile)

    email = kakao_account.get('email')
    print(email)
    nickname = profile.get('nickname')
    print(nickname)
    data = {
        "email":email,
        "nickname":nickname
    }
    with open("data.json",'w',encoding ="utf-8") as f:
        json.dump(data, f, ensure_ascii = False ,indent=4)
    return access_token
def get_user_info_from_kakao(token):
    url = "https://kapi.kakao.com/v2/user/me"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
    }
    try:
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()  # HTTP 오류가 발생하면 예외 처리
        user_info = response.json()
        return user_info
    except Exception as e:
        print("Error getting user info:", e)
        return None
