import os
import time
import random
import string
from datetime import datetime

def generate_random_word():
    word_length = random.randint(3, 10)
    return ''.join(random.choices(string.ascii_lowercase, k=word_length))

def create_random_word_file(timer, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    while True:
        time.sleep(timer)
    
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        random_word = generate_random_word()
        
        file_path = os.path.join(output_path, f"{timestamp}.txt")
        
        with open(file_path, 'w') as file:
            file.write(random_word)
        
        print(f"Created file: {file_path} with word: {random_word}")

timer = 1.0
output_path = "./data/"

create_random_word_file(timer, output_path)