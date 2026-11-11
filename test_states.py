import tkinter as tk
import time
from pet import Pet
root=tk.Tk(); app=Pet(root);root.update()
position=(root.winfo_x(),root.winfo_y())
def tick():
    root.after_cancel(app.after_id)
    app.animate();root.update()
assert app.visual_state()=='idle'
app.start_focus(25);tick()
assert app.visual_state()=='typing'
deadline=app.focus_deadline
app.feed();tick()
assert app.visual_state()=='feeding'
app.feed_started=time.monotonic()-3;tick();tick()
assert app.visual_state()=='typing' and app.focus_deadline==deadline
app.stop_focus();tick()
assert app.visual_state()=='idle'
app.sleep();tick()
assert app.visual_state()=='sleeping'
app.feed();tick()
assert app.visual_state()=='feeding'
app.feed_started=time.monotonic()-3;tick();tick()
assert app.visual_state()=='sleeping'
app.wake();tick()
assert app.visual_state()=='waking'
app.waking_until=time.monotonic()-1;tick()
assert app.visual_state()=='idle'
assert position==(root.winfo_x(),root.winfo_y())
for size in (200,280,360):
    app.load_size(size)
    assert app.typing_frames[0].width()==size
    assert app.prone_frames[0].height()==round(size*420/400)
print('PASS: idle/focus/feed/resume/sleep/wake transitions; focus deadline preserved; window anchor stable; all sizes')
app.quit()
