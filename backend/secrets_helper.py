# secrets_helper.py
import os
import json

def get_db_creds_from_env_or_dict():
    # fallback to environment variables
    return {
        "host": os.environ.get("DB_HOST"),
        "port": int(os.environ.get("DB_PORT", "3306")),
        "user": os.environ.get("DB_USER"),
        "password": os.environ.get("DB_PASS"),
        "db": os.environ.get("DB_NAME"),
    }
