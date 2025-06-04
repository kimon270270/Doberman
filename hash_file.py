import hashlib
import os
from database_update import database_call

def get_files(directory):
    files_list = []
    files = os.listdir(directory)
    
    for f in files:
        files_list.append(os.path.join(directory,f))
    
    return files_list


def generate_hash(files_list):
    
    hashes = []
    indexes = []

    for i, file in enumerate(files_list):
        try:
            with open(file, "rb") as f:
                file_content = f.read()
                h = hashlib.sha256()
                
                if (h):
                    indexes.append(i)
                
                h.update(file_content)
                
                hashes.append(h.hexdigest())
                               
        except Exception as e:
            print(f"File: {file}\t{e}\n")
            
    for j, i in enumerate(indexes):
        database_call(files_list[i], hashes[j])

if __name__ == "__main__":
    files = get_files(r"")
    generate_hash(files)