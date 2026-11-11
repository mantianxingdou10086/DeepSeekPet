import tkinter as tk
import time
from pet import Pet,ROOT
from desktop_runtime import DesktopRuntime,SETTINGS
backup=SETTINGS.read_bytes() if SETTINGS.exists() else None
r=tk.Tk();p=Pet(r);r.update();p.desktop=DesktopRuntime(p,ROOT)
try:
    p.start_focus(5);p.desktop.hide();p.say('discard this');r.update()
    assert p.bubble is None,'hidden pet created a bubble'
    p.update_focus(time.monotonic()+400);r.update()
    assert p.focus_deadline is None and p.bubble is None
    p.desktop.show();r.update()
    assert p.bubble is not None,'completion reminder not delivered on restore'
    assert '专注完成' in p.bubble.winfo_children()[0].cget('text')
    p.hide_bubble();p.desktop.hide();p.desktop.show();r.update()
    assert p.bubble is None,'completion reminder delivered twice'
    print('PASS hidden bubble suppression, independent focus completion, one deferred reminder')
finally:
    p.quit()
    if backup is None:SETTINGS.unlink(missing_ok=True)
    else:SETTINGS.write_bytes(backup)
