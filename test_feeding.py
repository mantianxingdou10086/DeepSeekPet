import tkinter as tk
import time
import json
from PIL import Image
from pet import Pet, ROOT

root=tk.Tk()
app=Pet(root)
root.update()
shots=[]
for t in [0,.35,.7,.95,1.3,1.9]:
    frame=app.render_feed(t)
    bg=Image.new('RGB',frame.size,'#dce7f2')
    bg.paste(frame,mask=frame.getchannel('A'))
    shots.append(bg)
shots[0].save(ROOT/'feeding-preview.gif',save_all=True,append_images=shots[1:],duration=[250,250,200,250,350,800],loop=0)
sheet=Image.new('RGB',(app.size*3,shots[0].height),'#dce7f2')
for col,i in enumerate([0,2,4]):sheet.paste(shots[i],(col*app.size,0))
sheet.save(ROOT/'feeding-check.png')
for i in range(3):
    app.feed()
    start=app.feed_started
    app.feed()
    assert app.feed_started==start, 'Overlapping feeds allowed'
    end=time.monotonic()+4
    while app.feed_started is not None and time.monotonic()<end:
        root.update()
        time.sleep(.015)
    assert app.feed_started is None, 'Feed did not complete'
    assert app.feed_finished==i+1
assert len(app.feed_times)==3
app.feed()
assert app.feed_started is None, 'Full cooldown did not block'
assert '吃饱' in app.bubble.winfo_children()[0].cget('text')
app.load_size(360)
assert app.render_feed(.4).size==(360,378)
print(json.dumps({'completed_feeds':app.feed_finished,'overlap_guard':'passed','full_response':'passed','resize':'passed','preview':str(ROOT/'feeding-preview.gif')},ensure_ascii=False))
app.quit()
