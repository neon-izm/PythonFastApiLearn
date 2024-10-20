from fastapi import FastAPI, Depends, HTTPException, status
from app.routers import users, todos
from app import auth, schemas, models, database
from sqlalchemy.orm import Session
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS設定の追加
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切なオリジンを指定してください
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(todos.router)

# データベースの初期化
models.Base.metadata.create_all(bind=database.engine)

# ログイン用のリクエストボディスキーマを定義
class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/token", response_model=schemas.Token)
def login(login_request: LoginRequest, db: Session = Depends(database.get_db)):
    email = login_request.email
    password = login_request.password
    logger.debug(f"Login attempt for user: {email}")
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        logger.debug("User not found.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="メールアドレスまたはパスワードが正しくありません",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not auth.verify_password(password, user.hashed_password):
        logger.debug("Password verification failed.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="メールアドレスまたはパスワードが正しくありません2",
            headers={"WWW-Authenticate": "Bearer"},
        )
    logger.debug("Authentication successful.")
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
