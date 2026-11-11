import tkinter as tk,time
from pet import Pet
r=tk.Tk();p=Pet(r);r.update()
p.sleep();p.wake()
assert p.visual_state()=='waking'
p.waking_until=time.monotonic()-1
assert p.visual_state()=='idle'
p.sleep();p.start_focus(5)
assert p.visual_state()=='typing'
p.stop_focus();p.sleep();p.feed()
assert p.visual_state()=='feeding'
assert p.restore_sleep_after_feed
print('PASS wake transition, expiry, focus/feed priority')
p.quit()
