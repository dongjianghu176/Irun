"""数据库会话与初始化。

SQLite 单文件，开箱即用；后续换 MySQL/PostgreSQL 只需改 DATABASE_URL。
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import DATABASE_URL

# SQLite 需要关闭同线程检查，FastAPI 多线程下才能正常用
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()


def get_db():
    """FastAPI 依赖注入：每个请求一个会话，结束自动关闭。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """建表（已存在则跳过）。导入所有模型后再调用。"""
    from . import models  # noqa: F401  确保模型被注册

    Base.metadata.create_all(bind=engine)
