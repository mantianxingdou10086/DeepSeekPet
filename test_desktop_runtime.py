import tkinter as tk
import subprocess,sys,time,ctypes
from pet import Pet,ROOT
from desktop_runtime import DesktopRuntime,acquire_instance,read_settings,SETTINGS
backup=SETTINGS.read_bytes() if SETTINGS.exists() else None
root=tk.Tk();app=Pet(root);root.update()
app.desktop=DesktopRuntime(app,ROOT)
try:
    app.load_size(200);app.auto_sleep=False
    root.geometry('+123+234');root.update();app.desktop.save()
    assert read_settings()['x']==123 and read_settings()['size']==200
    app.desktop.hide();root.update();assert root.state()=='withdrawn'
    app.desktop.commands.put('show');app.desktop.poll();root.update()
    assert root.state()=='normal'
    handle=acquire_instance();assert handle
    code='from desktop_runtime import acquire_instance; assert acquire_instance() is None; print("duplicate blocked")'
    r=subprocess.run([sys.executable,'-c',code],cwd=ROOT,capture_output=True,text=True)
    assert r.returncode==0,r.stderr
    api=ctypes.WinDLL('kernel32');api.CloseHandle.argtypes=[ctypes.c_void_p];api.CloseHandle(handle)
    print('PASS: real tray visible=',app.desktop.icon.visible,'; queued show/hide; disk settings; cross-process single instance')
finally:
    app.quit()
    if backup is None:SETTINGS.unlink(missing_ok=True)
    else:SETTINGS.write_bytes(backup)
