import hashlib
import os

def get_files(directory):
    files_list = []
    files = os.listdir(directory)
    
    for f in files:
        files_list.append(os.path.join(directory,f))
    
    return files_list

def generate_hash(files_list):
    hashes = []
    for file in files_list:
        try:
            with open(file, "rb") as f:
                file_content = f.read()
                h = hashlib.sha256()
                h.update(file_content)
                
                hashes.append(h.hexdigest())
                
        except Exception as e:
            print(f"File: {file}\t{e}\n")
            
    return(hashes)


if __name__ == "__main__":
    files = get_files(r"")
    generate_hash(files)
