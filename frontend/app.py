import streamlit as st
import requests

API_URL = "http://backend:8000"

st.title("Todo管理アプリ")

email = st.text_input("メールアドレス")
password = st.text_input("パスワード", type="password")

if st.button("ログイン"):
    response = requests.post(f"{API_URL}/token", data={"username": email, "password": password})
    if response.status_code == 200:
        token = response.json()["access_token"]
        st.success("ログイン成功")
    else:
        st.error("ログイン失敗")

if 'token' in locals():
    headers = {"Authorization": f"Bearer {token}"}
    todos_response = requests.get(f"{API_URL}/todos/", headers=headers)
    if todos_response.status_code == 200:
        todos = todos_response.json()
        for todo in todos:
            st.write(todo["title"])
