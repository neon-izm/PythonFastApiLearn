from fastapi import FastAPI
from .routers import users, todos, auth_routes
from . import models, database
import logging
# CORS設定の追加
from fastapi.middleware.cors import CORSMiddleware
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切なオリジンを指定してください
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの登録
app.include_router(users.router)
app.include_router(todos.router)
app.include_router(auth_routes.router) 

# データベースの初期化
models.Base.metadata.create_all(bind=database.engine)
