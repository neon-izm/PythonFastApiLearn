import streamlit as st
import requests

API_URL = "http://backend:8000"

st.title("Todo管理アプリ")

# セッション状態を保持するための初期化
if 'token' not in st.session_state:
    st.session_state['token'] = None

def login():
    email = st.session_state['login_email']
    password = st.session_state['login_password']
    data = {"email": email, "password": password}
    response = requests.post(
        f"{API_URL}/token",
        json=data  # JSON形式でデータを送信
    )
    if response.status_code == 200:
        st.session_state['token'] = response.json()["access_token"]
        st.success("ログイン成功")
    else:
        st.error("ログイン失敗")
        st.error(f"詳細: {response.text}")


def logout():
    st.session_state['token'] = None
    st.success("ログアウトしました")

def get_todos():
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    todos_response = requests.get(f"{API_URL}/todos/", headers=headers)
    if todos_response.status_code == 200:
        return todos_response.json()
    else:
        st.error("Todoの取得に失敗しました")
        return []

def create_todo():
    title = st.session_state['new_todo_title']
    description = st.session_state['new_todo_description']
    data = {
        "title": title,
        "description": description
    }
    headers = {
        "Authorization": f"Bearer {st.session_state['token']}",
        "Content-Type": "application/json"
    }
    response = requests.post(f"{API_URL}/todos/", json=data, headers=headers)
    if response.status_code == 200:
        st.success("Todoを追加しました")
        # フォームをリセット
        st.session_state['new_todo_title'] = ''
        st.session_state['new_todo_description'] = ''
    else:
        st.error("Todoの追加に失敗しました")
        st.error(f"詳細: {response.text}")

def register():
    email = st.session_state['register_email']
    password = st.session_state['register_password']
    data = {"email": email, "password": password}
    response = requests.post(
        f"{API_URL}/users/",
        json=data
    )
    if response.status_code == 200:
        st.success("ユーザー登録が成功しました。ログインしてください。")
    else:
        st.error("ユーザー登録に失敗しました")
        st.error(f"詳細: {response.text}")

if st.session_state['token']:
    st.button("ログアウト", on_click=logout)
    st.header("あなたのTodoリスト")

    todos = get_todos()
    for todo in todos:
        st.write(f"- {todo['title']}")

    st.subheader("新しいTodoを追加")
    st.text_input("タイトル", key='new_todo_title')
    st.text_area("説明", key='new_todo_description')
    st.button("追加", on_click=create_todo)

else:
    st.subheader("ログイン")
    st.text_input("メールアドレス", key='login_email')
    st.text_input("パスワード", type="password", key='login_password')
    st.button("ログイン", on_click=login)

    st.subheader("新規ユーザー登録")
    st.text_input("新しいメールアドレス", key='register_email')
    st.text_input("新しいパスワード", type="password", key='register_password')
    st.button("登録", on_click=register)
