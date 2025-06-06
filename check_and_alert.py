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
receiver_email = os.getenv("RECEIVER_EMAIL")
sender_key = os.getenv("SENDER_KEY")


def get_id():
    
    id_list = []
    
    try:
        with psycopg2.connect(port=DATABASE_PORT, database=POSTGRES_DB, user=POSTGRES_USER,password=POSTGRES_PASSWORD) as conn:
            with conn.cursor() as curr:
                
                count_script = """
                SELECT id 
                FROM hash_table;
                """
                
                curr.execute(count_script)
                
                result = curr.fetchall()
                
                for pk_id in result:
                    id_list.append(pk_id[0])             
        
    except Exception as e:
        print(f"GET_COUNT\t{e}")

    return id_list


def current_hash(file_path):
    
    try:
        if (os.path.exists(file_path)):
            with open (file_path, "rb") as f:
                file_content = f.read()
                
                
                h = hashlib.sha256()
                h.update(file_content)
                
        else:
            return("FileDeleted")
        
    except Exception as e:
        print(f"CURRENT_HASH\t{e}")
        
    return (h.hexdigest())


def check_hash(id_list):
    try:
        for i in id_list:
            with psycopg2.connect(port=DATABASE_PORT, database=POSTGRES_DB, user=POSTGRES_USER,password=POSTGRES_PASSWORD) as conn:
                with conn.cursor() as curr:
                    
                    select_script = """
                    SELECT path, hash 
                    FROM hash_table
                    WHERE id = %s;
                    """
                    curr.execute(select_script, (i,))
                    result = curr.fetchone()
                    file_path = result[0]
                    database_hash = result[1]
                    curr_hash = current_hash(file_path)
                    
                    if (curr_hash == "FileDeleted"):
                        text = f"Subject: File Deletion Alert\n\n{file_path} has been deleted."
                        server = smtplib.SMTP("smtp.gmail.com", 587)
                        server.starttls()
                        server.login(sender_email, sender_key)
                        server.sendmail(sender_email, receiver_email, text)
                        server.quit()
                        
                        print(f"Email Sent For Deletion of {file_path}.\n\n")
                        
                    
                    elif not (database_hash == curr_hash):
                        text = f"Subject: File Modification/Alteration Alert\n\n{file_path} has been modified/altered."
                        server = smtplib.SMTP("smtp.gmail.com", 587)
                        server.starttls()
                        server.login(sender_email, sender_key)
                        server.sendmail(sender_email, receiver_email, text)
                        server.quit()
                        
                        print(f"Email Sent For Modification/Alteration of {file_path}.\n\n")
                        
                    else:
                        print(f"No Alteration/Modification For {file_path}.\n\n")
                        
                        
                
        
    except Exception as e:
        print(f"CHECK_HASH\t{e}")
    
if __name__ == "__main__":
    id_list = get_id()
    check_hash(id_list)