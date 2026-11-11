import tkinter as tk,time
from pet import Pet
from motion_timing import WAKE_DURATION,wakeup_frame
r=tk.Tk();p=Pet(r);r.update()
try:
    assert len(p.wakeup_frames)==17, len(p.wakeup_frames)
    p.sleep();p.wake()
    for t in [0,.3,.7,1.,1.6,2.0,2.52,2.72,2.76,2.92,3.1]:
        if p.after_id:r.after_cancel(p.after_id)
        p.waking_until=time.monotonic()+WAKE_DURATION-t
        p.animate()
        assert str(p.label.cget('image'))==str(p.wakeup_frames[wakeup_frame(t)]),(t,p.label.cget('image'))
    for size in [200,280,360]:
        p.load_size(size);assert len(p.wakeup_frames)==17
        assert p.wakeup_frames[3].width()==size
    p.waking_until=0
    assert p.visual_state()=='idle'
    p.sleep();p.start_focus(5);assert p.visual_state()=='typing'
    p.stop_focus();p.sleep();p.eat_rice();assert p.visual_state()=='eating'
    print('PASS real Tk wake renderer, 17 frames, size changes, idle/focus/rice priority')
finally:p.quit()
