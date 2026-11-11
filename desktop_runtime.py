import os
import json
import ctypes
import queue
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

DATA=Path(os.environ.get('LOCALAPPDATA',Path.home()))/'DeepSeekPet'
SETTINGS=DATA/'settings.json'

def read_settings(path=SETTINGS):
    try:
        data=json.loads(path.read_text(encoding='utf-8'))
        return data if isinstance(data,dict) else {}
    except (OSError,ValueError):
        return {}

def write_settings(data,path=SETTINGS):
    path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_suffix('.tmp')
    temporary.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
    temporary.replace(path)

def acquire_instance():
    api=ctypes.WinDLL('kernel32',use_last_error=True)
    api.CreateMutexW.argtypes=[ctypes.c_void_p,ctypes.c_bool,ctypes.c_wchar_p]
    api.CreateMutexW.restype=ctypes.c_void_p
    handle=api.CreateMutexW(None,False,'Local\\DeepSeekPet.Desktop.v1')
    if not handle:
        raise ctypes.WinError(ctypes.get_last_error())
    if ctypes.get_last_error()==183:
        api.CloseHandle.argtypes=[ctypes.c_void_p]
        api.CloseHandle(handle)
        return None
    return handle

class DesktopRuntime:
    def __init__(self,app,root_path):
        import pystray
        from PIL import Image
        self.app=app
        self.commands=queue.Queue()
        self.closed=False
        self.hidden=False
        self.last_saved=None
        DATA.mkdir(parents=True,exist_ok=True)
        logging.basicConfig(level=logging.INFO,handlers=[RotatingFileHandler(DATA/'desktop.log',maxBytes=500000,backupCount=2,encoding='utf-8')])
        app.root.report_callback_exception=lambda *exc:logging.error('GUI callback failure',exc_info=exc)
        settings=read_settings()
        size=settings.get('size',280)
        if type(size) is int and size in (200,280,360):app.load_size(size)
        app.auto_sleep=settings.get('auto_sleep',True) is not False
        app.root.update_idletasks()
        x=settings.get('x',app.root.winfo_x()); y=settings.get('y',app.root.winfo_y())
        if type(x) is not int:x=0
        if type(y) is not int:y=0
        from window_bounds import place
        place(app.root,x,y,app.size,round(app.size*1.05))
        def action(name):
            return lambda icon,item:self.commands.put(name)
        self.icon=pystray.Icon('DeepSeekPet',Image.open(root_path/'pet.ico'),'DeepSeek 桌宠',pystray.Menu(
            pystray.MenuItem('显示桌宠',action('show'),default=True),
            pystray.MenuItem('隐藏桌宠',action('hide')),
            pystray.MenuItem('喂 Token',action('feed')),
            pystray.MenuItem('退出',action('quit'))))
        self.icon.run_detached()
        self.poll()

    def hide(self):
        self.save()
        self.hidden=True
        self.app.hide_bubble()
        self.app.root.withdraw()
        if self.app.focus_window:self.app.focus_window.withdraw()

    def show(self):
        self.hidden=False
        self.app.ensure_visible()
        self.app.root.deiconify()
        if self.app.focus_window:self.app.focus_window.deiconify()
        self.app.root.lift()
        if self.app.pending_reminder:
            text=self.app.pending_reminder
            self.app.pending_reminder=None
            self.app.say(text)

    def save(self):
        if self.hidden:return
        app=self.app
        data={'size':app.size,'x':app.root.winfo_x(),'y':app.root.winfo_y(),'auto_sleep':app.auto_sleep}
        if data!=self.last_saved:
            try:
                write_settings(data)
                self.last_saved=data
            except OSError:logging.exception('Cannot save preferences')

    def poll(self):
        if self.closed:return
        while not self.commands.empty():
            command=self.commands.get_nowait()
            if command=='quit':
                self.app.quit();return
            if command=='show':self.show()
            if command=='hide':self.hide()
            if command=='feed':self.show();self.app.feed()
        if not self.hidden:self.app.ensure_visible()
        self.save()
        self.poll_id=self.app.root.after(600,self.poll)

    def close(self):
        self.save()
        self.closed=True
        self.app.root.after_cancel(self.poll_id)
        self.icon.stop()
