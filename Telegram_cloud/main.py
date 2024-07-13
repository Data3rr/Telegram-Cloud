# MAIN FILE - FLASK SERVER

from flask import Flask, render_template, send_file, jsonify, request
from functions.download import download_file # module local (/functions)
from functions.upload import uploader # module local (/functions)
import json
import os

# Variable creation
app = Flask('app')  # creation of variable used by flask
state = "Online"  # creation of status variable (not very useful)

# Telegram bot information
TOKEN = ""  # your bot token
CHAT_ID = ""  # id of the channel to send files to



# <--- Auxiliary functions --->
def json_length() -> int:
    """Function to retrieve the length of the "register" json in order to
    to determine the number of files in the cloud"""
    with open('static/data/reg.json', 'r', encoding='utf-8') as reg_file:
        reg_data = json.load(reg_file)
        return len(reg_data)



# <--- Main functions (site pages) --->
@app.route('/')  # page: home / main page
def home_page():
    """Function for displaying index.html, i.e.
    the html of the site's main page"""
    return render_template('index.html',
                           file_number=json_length(),
                           state=state)


@app.route('/upload') # page: upload files to the cloud (interface)
def upload():
    """Function to display upload.html, i.e.
    the html page for uploading files to the cloud"""
    return render_template('upload.html')


@app.route('/download/<file_name>', methods=['GET']) # api: download
def start_download(file_name: str):
    """Function to start downloading a file,
    it must be called with a GET request containing the name of the file in question.
    in question, it is called from the js"""
    success, result = download_file(file_name, TOKEN)
    if not success:
        return jsonify({"error": result}), 400
    return send_file(result, as_attachment=True, download_name=file_name)


@app.route('/upload_file', methods=['POST']) # api: send files to the cloud (requete) 
def upload_file():
    """Function for sending files to the cloud. 
    be called by a post request containing the name and content of the file to be sent
    on the cloud, it is called by js"""
    data = request.json
    file_name = data.get('file_name')
    file_content = data.get('file_content')
    uploader(file_name, file_content, TOKEN, CHAT_ID)
    return jsonify({'message': 'Fichier envoye avec succes !'}), 200


# <--- Call to launch flask interface --->
if __name__ == "__main__":
    os.system('title Telegram Cloud')
    os.system('cls')
    print(f"""████████╗███████╗██╗     ███████╗ ██████╗ ██████╗  █████╗ ███╗   ███╗     ██████╗██╗      ██████╗ ██╗   ██╗██████╗ 
╚══██╔══╝██╔════╝██║     ██╔════╝██╔════╝ ██╔══██╗██╔══██╗████╗ ████║    ██╔════╝██║     ██╔═══██╗██║   ██║██╔══██╗
   ██║   █████╗  ██║     █████╗  ██║  ███╗██████╔╝███████║██╔████╔██║    ██║     ██║     ██║   ██║██║   ██║██║  ██║
   ██║   ██╔══╝  ██║     ██╔══╝  ██║   ██║██╔══██╗██╔══██║██║╚██╔╝██║    ██║     ██║     ██║   ██║██║   ██║██║  ██║
   ██║   ███████╗███████╗███████╗╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║    ╚██████╗███████╗╚██████╔╝╚██████╔╝██████╔╝
   ╚═╝   ╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝     ╚═════╝╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝\nby Adapters | Pls don't SKID/PASTA\n----\n""")
    app.run(host='0.0.0.0', port=8080)
