print('  _  _  ___  ___  ___    ___  ___  _  _  _____  ___  ___ ')
print(' | || ||_ _|| _ \| __|  / __|| __|| \| ||_   _|| _ \| __|')
print(' | __ | | | |   /| _|  | (__ | _| | .` |  | |  |   /| _| ')
print(' |_||_||___||_|_\|___|  \___||___||_|\_|  |_|  |_|_\|___|')  
print(' .....................GOOD MORNING!......................')
print('')

import subprocess
import webbrowser
import os
import json
import time
from backup import FileBackup
import threading


backup = FileBackup('settings.json')
backup_thread = threading.Thread(target=backup.run)
backup_thread.start()


with open('settings.json') as f:
    settings = json.load(f)


start_path = "C:\\Users\\fr4nk\\OneDrive\\Desktop\\start"
start_command = f'cmd /k "cd /d {start_path} /env/Scripts && activate && cd /d {start_path} && genauto.py"'
genauto_process = subprocess.Popen(start_command, shell=True)




fastapi_path = settings['fastapi_path']
start_command = f'cmd /k "cd /d {fastapi_path} /env/Scripts && activate && cd /d {fastapi_path} &&  uvicorn src.main:app --reload --port 5000"'
fastapi_process = subprocess.Popen(start_command, shell=True)
time.sleep(20)
os.chdir(settings['angular_path'])
angular_process = subprocess.Popen('ng serve', shell=True)
time.sleep(20)
webbrowser.open_new(settings['web_url'])

fastapi_process.wait()
angular_process.wait()
genauto_process.wait()

