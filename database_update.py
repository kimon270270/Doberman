import psycopg2
import os
from dotenv import load_dotenv


load_dotenv(override=True)

DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_USER = os.getenv('POSTGRES_USER')


def add_hash(file, hash_key):
    try:
        with psycopg2.connect(port=DATABASE_PORT, database=POSTGRES_DB, user=POSTGRES_USER,password=POSTGRES_PASSWORD) as conn:
            with conn.cursor() as curr:
                
                add_script = """
                INSERT INTO (path, hash, created, last_modified) hash_table 
                VALUES (%s,%s,NOW(),NOW())"""
                
                curr.execute(add_script, (file, hash_key))
                
        
    except Exception as e:
        print(f"ADD_HASH\t{e}")


def update_hash(pk_id, hash_key):
    try:
        with psycopg2.connect(port=DATABASE_PORT, database=POSTGRES_DB, user=POSTGRES_USER,password=POSTGRES_PASSWORD) as conn:
            with conn.cursor() as curr:
                
                update_script = """
                UPDATE hash_table 
                SET hash = %s, last_modified = NOW() 
                WHERE id = %s"""
                
                curr.execute(update_script, (hash_key,pk_id,))
                
        
    except Exception as e:
        print(f"UPDATE_HASH\t{e}")


def add_or_update(file, hash_key):    
    try:
        with psycopg2.connect(port=DATABASE_PORT, database=POSTGRES_DB, password=POSTGRES_PASSWORD, user=POSTGRES_USER) as conn:
            
            with conn.cursor() as curr:
                
                select_script = """
                SELECT id 
                FROM hash_table 
                WHERE path = %s"""
                
                curr.execute(select_script, (file,))
                pk_id = curr.fetchone()
        
        if (pk_id):
            update_hash(file, hash_key)
            
        else:
            add_hash(pk_id, hash_key)
                
    except Exception as e:
        print(f"ADD_OR_UPDATE\t{e}")
        

if __name__ == "__main__":
    add_or_update("file", "hash_key")