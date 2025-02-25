import os
import time
import py7zr

def monitor_and_chunk(input_path, output_path, treshold, chunk):
    if not os.path.exists(input_path):
        os.makedirs(input_path)
        print(f"Created input directory: {input_path}")
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"Created output directory: {output_path}")
    
    chunk = min(chunk, treshold)
    
    while True:
        try:
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
        
        except Exception as e:
            print(f"An error occurred: {e}")
        
        time.sleep(1)

input_path = "./data"
treshold = 10
chunk = 10
output_path = "./compressed"

monitor_and_chunk(input_path, output_path, treshold, chunk)
