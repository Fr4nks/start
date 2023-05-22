
from pywinauto.application import Application

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
        app = Application(backend="win32").connect(path=r"C:\Users\fr4nk\OneDrive\Desktop\Genhire\GHFB.exe", title="Genhire")
        app.windows()
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
        app = Application(backend="win32").start(r"C:\Users\fr4nk\OneDrive\Desktop\Genhire\GHFB.exe")
        print('Genhire us starting...')
        login(app)
        print('Genhire is logging in...')
        return app
    except:
        print('Genhire failed to open')

connect_genhire()