import tkinter as tk
import time
from pet import Pet

root=tk.Tk()
app=Pet(root)
root.update()
app.sleep()
app.start_focus(25)
assert not app.sleeping
assert app.focus_deadline > time.monotonic()+1490
app.last_interaction=time.monotonic()-400
root.after_cancel(app.after_id)
app.animate()
assert not app.sleeping, 'Focus must prevent automatic sleep'
assert app.focus_window.winfo_exists()
app.feed()
assert app.focus_deadline is not None
app.feed_started=None
app.focus_deadline=time.monotonic()-1
root.after_cancel(app.after_id)
app.animate()
assert app.focus_deadline is None
assert app.focus_window is None
assert '休息' in app.bubble.winfo_children()[0].cget('text')
app.start_focus(5)
app.stop_focus()
assert app.focus_deadline is None and app.focus_window is None
print('PASS: start, wake, idle inhibition, feeding compatibility, expiry reminder, cancel')
app.quit()
