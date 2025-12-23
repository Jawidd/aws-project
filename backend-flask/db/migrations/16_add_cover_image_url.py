#!/usr/bin/env python3

import psycopg2
import os
import sys

current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, '..', '..', '..'))
sys.path.append(parent_path)
from lib.db import db

def migrate_sql():
    return """
    ALTER TABLE public.users 
    ADD COLUMN IF NOT EXISTS cover_image_url VARCHAR(500);
    """

def rollback_sql():
    return """
    ALTER TABLE public.users 
    DROP COLUMN IF EXISTS cover_image_url;
    """

def migrate():
    print("== db-migrate: Adding cover_image_url column ==")
    try:
        with db.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(migrate_sql())
                conn.commit()
        print("Migration completed successfully")
    except Exception as e:
        print(f"Migration failed: {e}")
        raise

def rollback():
    print("== db-rollback: Removing cover_image_url column ==")
    try:
        with db.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(rollback_sql())
                conn.commit()
        print("Rollback completed successfully")
    except Exception as e:
        print(f"Rollback failed: {e}")
        raise

if __name__ == "__main__":
    migrate()