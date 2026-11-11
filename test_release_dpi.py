import tkinter as tk
import ctypes
from ctypes import wintypes
from window_bounds import work_areas
r=tk.Tk();r.withdraw()
try:
    raw=wintypes.RECT();assert ctypes.windll.user32.SystemParametersInfoW(48,0,ctypes.byref(raw),0)
    areas=work_areas(r)
    primary=next(a for a in areas if a[0]>=raw.left and a[0]<raw.right and a[1]>=raw.top and a[1]<raw.bottom)
    assert primary[2]<=raw.right-2 and primary[3]<=raw.bottom-2,'fractional DPI needs rounding guard'
    print('PASS work area has 2 logical pixel fractional-DPI safety margin')
finally:r.destroy()
