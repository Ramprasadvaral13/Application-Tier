# db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from secrets_helper import get_db_creds_from_env_or_dict

_creds = get_db_creds_from_env_or_dict()
DB_URL = f"mysql+pymysql://{_creds['user']}:{_creds['password']}@{_creds['host']}:{_creds['port']}/{_creds['db']}?charset=utf8mb4"

# Pool settings for production-ish
engine = create_engine(DB_URL, pool_size=10, max_overflow=20, pool_recycle=3600, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
