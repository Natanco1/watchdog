import os
import time
import py7zr

def monitor_and_chunk(input_path, output_path, treshold, chunk):
    while True:
        files = sorted(os.listdir(input_path)) 
        files = [f for f in files if os.path.isfile(os.path.join(input_path, f))]
        
        if len(files) >= treshold:
            chunk_files = files[:chunk]
            
            first_file = chunk_files[0]
            last_file = chunk_files[-1]
            archive_name = f"{first_file.split('.')[0]}_{last_file.split('.')[0]}.7z"
            archive_path = os.path.join(output_path, archive_name)
            
            with py7zr.SevenZipFile(archive_path, 'w') as archive:
                for file in chunk_files:
                    file_path = os.path.join(input_path, file)
                    archive.write(file_path, arcname=file)
            
            print(f"Created archive: {archive_path} containing {len(chunk_files)} files.")
            
            for file in chunk_files:
                os.remove(os.path.join(input_path, file))
                print(f"Removed file: {file}")
        
        time.sleep(5)

input_path = "./data"
treshold = 10
chunk = 10
output_path = "./compressed"

monitor_and_chunk(input_path, output_path, treshold, chunk)
