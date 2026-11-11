import tkinter as tk
import time
from pet import Pet
r=tk.Tk();p=Pet(r);r.update()
def tick():
    r.after_cancel(p.after_id);p.animate();r.update()
try:
    assert callable(getattr(p,'eat_rice',None)), 'Rice action is missing'
    p.eat_rice(); assert p.visual_state()=='eating'
    start=p.rice_started;p.eat_rice();assert p.rice_started==start
    p.feed();assert p.feed_started is None
    p.rice_started=time.monotonic()-10;tick();assert p.visual_state()=='idle'
    p.sleep();p.eat_rice();assert p.visual_state()=='eating'
    p.rice_started=time.monotonic()-10;tick();assert p.visual_state()=='sleeping'
    p.start_focus(5);deadline=p.focus_deadline;p.eat_rice()
    p.rice_started=time.monotonic()-10;tick();assert p.visual_state()=='typing'
    assert p.focus_deadline==deadline
    p.stop_focus();p.eat_rice();p.sleep()
    assert p.visual_state()=='eating'
    p.rice_started=time.monotonic()-10;tick();assert p.visual_state()=='sleeping'
    for size in (200,280,360):
        p.load_size(size);assert p.rice_frames[0].width()==size
    print('PASS rice entry, overlap guard, token exclusion, completion, sleep restoration, focus preservation, queued sleep, sizes')
finally:p.quit()
