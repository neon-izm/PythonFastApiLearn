import streamlit as st
import requests
from typing import Optional

# APIのエンドポイントの設定
API_BASE_URL = "http://backend:8000"

def setup_session_state():
    if 'session' not in st.session_state:
        st.session_state['session'] = {'access_token': None, 'refresh_token': None, 'user_email': None}

def get_headers():
    access_token = st.session_state['session']['access_token']
    return {"Authorization": f"Bearer {access_token}"} if access_token else {}

def authenticate(email: str, password: str, endpoint: str):
    response = requests.post(f"{API_BASE_URL}/{endpoint}", json={"email": email, "password": password})
    if response.status_code == 200:
        update_session_state(response.json(), email)
        st.rerun()
    else:
        st.error("認証に失敗しました。")
        st.error(response.json().get('detail', '詳細情報が提供されていません。'))

def update_session_state(data: dict, email: str):
    st.session_state['session']['access_token'] = data['access_token']
    st.session_state['session']['refresh_token'] = data['refresh_token']
    st.session_state['session']['user_email'] = email

def logout():
    for key in ['access_token', 'refresh_token', 'user_email']:
        st.session_state['session'][key] = None
    st.info("ログアウトしました。")
    st.rerun()

def display_todos():
    response = api_request("GET", "/todos/")
    if response.status_code == 200:
        todos = response.json()
        if todos:
            st.write("あなたのToDoリスト：")
            for todo in todos:
                st.write(f"- {todo['title']}")
        else:
            st.write("ToDoがありません。")
    else:
        st.error("ToDoの取得に失敗しました。")

def display_todo_form():
    new_todo = st.text_input("新しいToDoを入力", key="new_todo")
    if st.button("ToDoを追加") and new_todo:
        response = api_request("POST", "/todos/", json={"title": new_todo})
        if response.status_code == 200:
            st.success("ToDoを追加しました。")
            st.rerun()
        else:
            st.error("ToDoの追加に失敗しました。")

def api_request(method: str, endpoint: str, **kwargs):
    """ APIリクエストを送信し、アクセストークンの有効期限が切れていた場合はリフレッシュを試みる """
    headers = get_headers()
    response = requests.request(method, f"{API_BASE_URL}{endpoint}", headers=headers, **kwargs)
    
    # アクセストークンが期限切れの場合
    if response.status_code == 401:
        # トークンのリフレッシュを試みる
        if refresh_access_token():
            # リフレッシュ成功後、再度リクエストを送信
            headers = get_headers()
            response = requests.request(method, f"{API_BASE_URL}{endpoint}", headers=headers, **kwargs)
        else:
            # リフレッシュに失敗した場合はログアウト
            logout()
    
    return response

def refresh_access_token() -> bool:
    """ リフレッシュトークンを使用してアクセストークンを更新 """
    refresh_token = st.session_state['session']['refresh_token']
    if not refresh_token:
        return False
    
    headers = {"Authorization": f"Bearer {refresh_token}"}
    response = requests.post(f"{API_BASE_URL}/refresh_token", headers=headers)
    
    if response.status_code == 200:
        st.session_state['session']['access_token'] = response.json()['access_token']
        st.success("アクセストークンを更新しました。")
        return True
    else:
        st.error("セッションの有効期限が切れました。再度ログインしてください。")
        return False

def main():
    setup_session_state()
    if not st.session_state['session']['access_token']:
        st.title("ログイン / ユーザー登録")
        email = st.text_input("メールアドレス", key="email")
        password = st.text_input("パスワード", type="password", key="password")
        if st.button("ログイン"):
            authenticate(email, password, "token_json")
        if st.button("ユーザー登録"):
            authenticate(email, password, "users/")
    else:
        st.title(f"ようこそ、{st.session_state['session']['user_email']}さん！")
        display_todos()
        display_todo_form()
        if st.button("ログアウト"):
            logout()

if __name__ == "__main__":
    main()
