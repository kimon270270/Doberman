import smtplib
import hashlib
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_USER = os.getenv('POSTGRES_USER')

sender_email = os.getenv("SENDER_EMAIL")
receiver_email = os.getenv("RECIEVER_EMAIL")
sender_key = os.getenv("SENDER_KEY")


def get_count():
    
    try:
        with psycopg2.connect(port=DATABASE_PORT, database=POSTGRES_DB, user=POSTGRES_USER,password=POSTGRES_PASSWORD) as conn:
            with conn.cursor() as curr:
                
                count_script = """
                SELECT COUNT(id) 
                FROM hash_table;
                """
                
                curr.execute(count_script)
                
                result = curr.fetchone
                count = result[0]
                
        
    except Exception as e:
        print(f"GET_COUNT\t{e}")

    return count


def current_hash(file_path):
    
    try:
        with open (file_path, "rb") as f:
            file_content = f.read()
            
            h = hashlib.sha256()
            h.update(file_content)
    
    except Exception as e:
        print(f"CURRENT_HASH\t{e}")
        
    return (h.hexdigest())

def check_hash(count):
    try:
        for i in range(count):
            with psycopg2.connect(port=DATABASE_PORT, database=POSTGRES_DB, user=POSTGRES_USER,password=POSTGRES_PASSWORD) as conn:
                with conn.cursor() as curr:
                    
                    select_script = """
                    SELECT path, hash 
                    FROM hash_table
                    WHERE id = %s;
                    """
                    
                    curr.execute(select_script, (i,))
                    
                    result = curr.fetchone
                    file_path = result[0]
                    database_hash = result[1]
                    
                    curr_hash = current_hash(file_path)
                    
                    if not (database_hash == curr_hash):
                        text = f"Subject: File Modification/Alteration Alert\n\nContents of {file_path} has been modified/altered."
                        server = smtplib.SMTP("smtp.gmail.com", 587)
                        server.starttls
                        
                        server.login(sender_email, sender_key)
                        server.sendmail(sender_email, receiver_email, text)
                        
                        print(f"Email Sent.")
                        
                    else:
                        print(f"No Alteration/Modification For {file_path}.\n")
                        
                        
                
        
    except Exception as e:
        print(f"CHECK_HASH\t{e}")
    
if __name__ == "__main__":
    count = get_count()
    check_hash(count)