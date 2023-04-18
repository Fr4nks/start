print('  _  _  ___  ___  ___    ___  ___  _  _  _____  ___  ___ ')
print(' | || ||_ _|| _ \| __|  / __|| __|| \| ||_   _|| _ \| __|')
print(' | __ | | | |   /| _|  | (__ | _| | .` |  | |  |   /| _| ')
print(' |_||_||___||_|_\|___|  \___||___||_|\_|  |_|  |_|_\|___|')  
print(' .....................GOOD MORNING!......................')
print('')



from pywinauto.application import Application
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

def login(app, name='FR', password='FRA'):
    try:
        app.TfmLogin.set_focus()
        app.TfmLogin.TBtnWinControl2.click()
        app.TwwLookupDlg.TwwDBGrid.set_focus()
        app.TwwLookupDlg.TwwIncrementalSearch1.type_keys('{BACKSPACE}{BACKSPACE}{BACKSPACE}{BACKSPACE}')
        app.TwwLookupDlg.TwwIncrementalSearch1.type_keys(name)
        app.TwwLookupDlg.TBitBtn2.click()
        app.TfrmLogin.TEdit1.type_keys(password)
        app.TfrmLogin.TBitBtn2.click()
    except:
        print('Genhire already open')


def connect_genhire():
    try:
        app = Application(backend="win32").connect(path=r"Z:\GHFB.exe", title="Genhire")
        app.Tfmain.set_focus()
        print('Genhire is running...')
        print('Are we logid in?')
        loged_in = app.Tfmain.is_visible()
        if loged_in is False:
            print('No')
            login(app)
        else:
            print('Yes')
        return app
    except:
        print('Genhire is not open, Try to start')
        pass
    try:
        app = Application(backend="win32").start(r"Z:\GHFB.exe")
        print('Genhire us starting...')
        login(app)
        print('Genhire is logging in...')
        return app
    except:
        print('Genhire failed to open')

connect_genhire()

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

