import tkinter as tk,time
from unittest.mock import patch
from pet import Pet
r=tk.Tk();p=Pet(r);r.update()
try:
    for action,stamp in [(p.feed,'feed_started'),(p.eat_rice,'rice_started'),(lambda:(p.sleep(),p.wake()),'waking_until')]:
        p.feed_started=p.rice_started=None;p.waking_until=0
        action()
        r.after_cancel(p.after_id);p.animate()
        before=p.label.cget('image');p.toggle_pause()
        old=getattr(p,stamp);base=p.motion_last
        with patch('pet.time.monotonic',return_value=base+10):
            r.after_cancel(p.after_id);p.animate()
            assert p.label.cget('image')==before,'paused effect changed frame'
            assert abs(getattr(p,stamp)-old-10)<0.1,'paused effect elapsed instead of freezing'
            p.toggle_pause()
        p.motion_last=time.monotonic()
    p.feed_started=p.rice_started=None;p.start_focus(5);p.toggle_pause()
    p.update_focus(time.monotonic()+301)
    assert p.focus_deadline is None,'animation pause stopped focus timer'
    print('PASS pause freezes feed/rice/wake effects; focus timer independent')
finally:p.quit()
