# MODULE - UPLOAD - functions.upload

import requests
import json

def split_file(file_content: str, chunk_size=20) -> str:
    """Function to split files if they are too large 
    so that they don't exceed the telegram limit"""
    chunk_size = int(chunk_size * 1024 * 1024)
    split_bytes = []
    offset = 0
    while offset < len(file_content):
        chunk = file_content[offset:offset + chunk_size]
        split_bytes.append(chunk)
        offset += chunk_size
    return split_bytes

def uploader(file_name: str, file_content: str, TOKEN: str, CHAT_ID: str) -> bool:
    """Function to send a file on the telegram channel
    via Telegram API"""
    url = f'https://api.telegram.org/bot{TOKEN}/sendDocument'
    with open("static/data/reg.json", "r", encoding='utf-8') as reg:
        reg_data = json.load(reg)
    try:
        test = reg_data[file_name]
        return False
    except:
        file_part = split_file(file_content)
        parts_reg = []
        for file_n in range(len(file_part)):
            data = {
                'chat_id': CHAT_ID,
                'parse_mode': 'HTML',
                'caption': f"{file_n}?{file_name}"
            }

            files = {'document': file_part[file_n]}

            try:
                r = requests.post(url, data=data, files=files, stream=True)
                r.raise_for_status()
                parts_reg.append(r.json()["result"]["document"])
            except requests.exceptions.RequestException as e:
                print(f"Erreur lors de l'envoie de la partie {file_n}: {e}")
                return False
        new_element = {file_name: [parts_reg]}
        reg_data.append(new_element)
        with open("static/data/reg.json", "w", encoding='utf-8') as reg:
            json.dump(reg_data, reg, indent=4)

        return True