import os
import time
import py7zr
from datetime import datetime

def monitor_and_chunk(input_path, output_path, threshold, chunk, expiration_seconds):
    if not os.path.exists(input_path):
        os.makedirs(input_path)
        print(f"Created input directory: {input_path}")
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"Created output directory: {output_path}")
    
    chunk = min(chunk, threshold)
    
    while True:
        try:
            files = sorted(os.listdir(input_path)) 
            files = [f for f in files if os.path.isfile(os.path.join(input_path, f))]
            
            expired_files = []
            current_time = datetime.now()
            for file in files:
                file_path = os.path.join(input_path, file)
                file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                if (current_time - file_mtime).total_seconds() > expiration_seconds:
                    expired_files.append(file)
            
            if len(expired_files) >= threshold:
                chunk_files = expired_files[:chunk]
                
                first_file_base = "".join(chunk_files[0].rsplit(".", 1)[:-1])
                last_file_base = "".join(chunk_files[-1].rsplit(".", 1)[:-1])
                folder_name = f"{first_file_base}_{last_file_base}"
                archive_name = f"{folder_name}.7z"
                archive_path = os.path.join(output_path, archive_name)
                
                with py7zr.SevenZipFile(archive_path, 'w') as archive:
                    for file in chunk_files:
                        file_path = os.path.join(input_path, file)
                        archive.write(file_path, arcname=file)
                
                print(f"Created archive: {archive_path} containing {len(chunk_files)} files.")
                
                for file in chunk_files:
                    os.remove(os.path.join(input_path, file))
                    print(f"Removed file: {file}")
        
        except Exception as e:
            print(f"An error occurred: {e}")
        
        time.sleep(1)

input_path = "./data"
threshold = 5
chunk = 5
output_path = "./compressed"
expiration_seconds = 10

monitor_and_chunk(input_path, output_path, threshold, chunk, expiration_seconds)