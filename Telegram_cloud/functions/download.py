# MODULE - DOWNLOAD - functions.donwload

from io import BytesIO
import requests
import json

#<--- Fonctions du module ---> 
def download_file(file_name: str, TOKEN: str):  
    """Function to download a file using the token of the telegram bot 
    and the name of the file (the file must be in the registry and in the bot's channel)"""
    url = f'https://api.telegram.org/bot{TOKEN}/getFile'

    with open("static/data/reg.json", "r", encoding='utf-8') as reg:
        reg_data = json.load(reg)
    try:
        for obj in reg_data:
            if file_name in obj:
                file_parts = obj[file_name]
                break

    except KeyError:
        return False, "File not found."

    file_data = BytesIO() # lit le fichier en bytes
    for part in file_parts:
        part_id = part[0]['file_id']

        response = requests.get(url, params={'file_id': part_id})
        response.raise_for_status()
        file_path = response.json().get('result', {}).get('file_path')
        if not file_path:
            return False, f"Error retrieving file path for part {part_id}."

        download_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_path}'

        # download the file with a request 
        try:
            with requests.get(download_url, stream=True) as r:
                r.raise_for_status()
                for chunk in r.iter_content(chunk_size=1024):
                    file_data.write(chunk)
        except requests.exceptions.RequestException as e:
            return False, f"Error downloading file part {part_id}: {e}"

    file_data.seek(0)  # reset file pointer to avoid bugs
    return True, file_data