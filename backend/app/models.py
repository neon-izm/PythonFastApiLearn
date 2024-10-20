from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)  # 長さを指定
    hashed_password = Column(String(255))                 # 長さを指定

    todos = relationship("Todo", back_populates="owner")

class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))          # 長さを指定
    description = Column(String(1024))   # 長さを指定（必要に応じて変更）
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates="todos")
