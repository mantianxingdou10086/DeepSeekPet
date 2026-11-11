import tkinter as tk
import time
from types import SimpleNamespace
from PIL import Image
from pet import Pet, ROOT

root=tk.Tk()
app=Pet(root)
root.update()
app.last_interaction=time.monotonic()-301
# 手动执行一次调度，先取消旧回调，避免重复动画循环。
root.after_cancel(app.after_id)
app.animate()
assert app.sleeping, 'No automatic sleep after pet inactivity'
shots=[]
for t in [0,.5,1,1.5,2]:
    frame=app.render_sleep(t)
    bg=Image.new('RGB',frame.size,'#dce7f2')
    bg.paste(frame,mask=frame.getchannel('A'))
    shots.append(bg)
shots[0].save(ROOT/'sleep-preview.gif',save_all=True,append_images=shots[1:],duration=500,loop=0)
app.press(SimpleNamespace(x_root=root.winfo_x()+100,y_root=root.winfo_y()+100))
app.release(None)
assert not app.sleeping
assert '醒' in app.bubble.winfo_children()[0].cget('text')
app.sleep()
assert app.sleeping
app.feed()
assert not app.sleeping and app.feed_started is not None
app.feed_started=None
app.auto_sleep=False
app.last_interaction=time.monotonic()-301
root.after_cancel(app.after_id)
app.animate()
assert not app.sleeping
app.sleep()
app.load_size(200)
assert app.render_sleep(.5).size==(200,210)
app.toggle_pause()
assert app.paused
print('PASS: auto sleep, click wake, feed wake, disable auto, manual sleep, resizing, pause')
app.quit()
