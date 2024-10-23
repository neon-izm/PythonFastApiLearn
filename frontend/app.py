import streamlit as st
import requests
from typing import Optional

# APIのエンドポイント
API_BASE_URL = "http://backend:8000"

# セッションステートでトークンを管理
if 'access_token' not in st.session_state:
    st.session_state['access_token'] = None
if 'refresh_token' not in st.session_state:
    st.session_state['refresh_token'] = None
if 'user_email' not in st.session_state:
    st.session_state['user_email'] = None

# ヘッダーの作成
def get_headers(token: Optional[str]) -> dict:
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

def register():
    email = st.session_state['reg_email']
    password = st.session_state['reg_password']
    response = requests.post(
        f"{API_BASE_URL}/users/",
        json={"email": email, "password": password}
    )
    if response.status_code == 200:
        data = response.json()
        st.session_state['access_token'] = data['access_token']
        st.session_state['refresh_token'] = data['refresh_token']
        st.session_state['user_email'] = email
        st.success("ユーザー登録に成功しました")
        st.rerun()
    else:
        st.error("ユーザー登録に失敗しました")

# ログイン処理
def login():
    email = st.session_state['login_email']
    password = st.session_state['login_password']
    response = requests.post(
        f"{API_BASE_URL}/token_json",
        json={"email": email, "password": password}
    )
    if response.status_code == 200:
        data = response.json()
        st.session_state['access_token'] = data['access_token']
        st.session_state['refresh_token'] = data['refresh_token']
        st.session_state['user_email'] = email
        st.success("ログイン成功")
        st.rerun()
    else:
        st.error("ログイン失敗")
        st.error(f"詳細: {response.text}")

# アクセストークンのリフレッシュ
def refresh_access_token():
    headers = get_headers(st.session_state['refresh_token'])
    response = requests.post(f"{API_BASE_URL}/refresh_token", headers=headers)
    if response.status_code == 200:
        data = response.json()
        st.session_state['access_token'] = data['access_token']
        st.success("アクセストークンを更新しました")
    else:
        st.error("セッションの有効期限が切れました。再度ログインしてください。")
        logout()

# ログアウト処理
def logout():
    st.session_state['access_token'] = None
    st.session_state['refresh_token'] = None
    st.session_state['user_email'] = None
    st.success("ログアウトしました")
    st.rerun()

# APIリクエストのヘルパー関数
def api_request(method: str, endpoint: str, **kwargs):
    headers = get_headers(st.session_state['access_token'])
    url = f"{API_BASE_URL}{endpoint}"
    response = requests.request(method, url, headers=headers, **kwargs)
    if response.status_code == 401:
        # アクセストークンの有効期限切れ
        refresh_access_token()
        headers = get_headers(st.session_state['access_token'])
        response = requests.request(method, url, headers=headers, **kwargs)
    return response

# メイン処理
def main():
    if st.session_state['access_token'] is None:
        st.title("ログイン / ユーザー登録")
        st.write("streamlit -version", st.__version__) 
        tab1, tab2 = st.tabs(["ログイン", "ユーザー登録"])

        with tab1:
            st.text_input("メールアドレス", key="login_email")
            st.text_input("パスワード", type="password", key="login_password")
            st.button("ログイン", on_click=login)

        with tab2:
            st.text_input("メールアドレス", key="reg_email")
            st.text_input("パスワード", type="password", key="reg_password")
            st.button("ユーザー登録", on_click=register)
    else:
        st.title("ToDoアプリ")
        st.write(f"ようこそ、{st.session_state['user_email']} さん")

        # ToDoの一覧を取得
        if st.button("ToDoを取得"):
            response = api_request("GET", "/todos/")
            if response.status_code == 200:
                todos = response.json()
                if todos:
                    st.write("あなたのToDoリスト：")
                    for todo in todos:
                        st.write(f"- {todo['title']}")
                else:
                    st.write("ToDoがありません")
            else:
                st.error("ToDoの取得に失敗しました")

        # ToDoの追加
        new_todo = st.text_input("新しいToDoを入力", key="new_todo")
        if st.button("ToDoを追加"):
            if new_todo:
                response = api_request("POST", "/todos/", json={"title": new_todo})
                if response.status_code == 200:
                    st.success("ToDoを追加しました")
                    st.session_state['new_todo'] = ""  # 入力欄をクリア
                else:
                    st.error("ToDoの追加に失敗しました")
            else:
                st.warning("ToDoを入力してください")

        # ログアウト
        if st.button("ログアウト"):
            logout()

if __name__ == "__main__":
    main()
