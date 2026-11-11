"""Windows work areas in Tk's coordinate space (system DPI awareness).
Negative coordinates are legitimate; never clamp against virtual bounding-box gaps.
"""
import ctypes
from ctypes import wintypes


def work_areas(root):
    result=[]
    if hasattr(ctypes, 'windll'):
        class MonitorInfo(ctypes.Structure):
            _fields_=[('cbSize',wintypes.DWORD),('rcMonitor',wintypes.RECT),
                      ('rcWork',wintypes.RECT),('dwFlags',wintypes.DWORD)]
        callback=ctypes.WINFUNCTYPE(wintypes.BOOL,wintypes.HMONITOR,wintypes.HDC,
                                   ctypes.POINTER(wintypes.RECT),wintypes.LPARAM)
        def collect(handle,dc,rect,data):
            info=MonitorInfo();info.cbSize=ctypes.sizeof(info)
            if ctypes.windll.user32.GetMonitorInfoW(handle,ctypes.byref(info)):
                r=info.rcWork
                # Tk/system-DPI rounding can overshoot a physical edge by 1 px.
                result.append((r.left+2,r.top+2,r.right-2,r.bottom-2))
            return True
        ctypes.windll.user32.EnumDisplayMonitors(None,None,callback(collect),0)
    return result or [(0,0,root.winfo_screenwidth(),root.winfo_screenheight())]


def clamp_rect(x,y,width,height,areas):
    def score(a):
        l,t,r,b=a
        overlap=max(0,min(x+width,r)-max(x,l))*max(0,min(y+height,b)-max(y,t))
        cx=min(max(x+width/2,l),r);cy=min(max(y+height/2,t),b)
        return (-overlap,(cx-x-width/2)**2+(cy-y-height/2)**2)
    l,t,r,b=min(areas,key=score)
    return (max(l,min(x,max(l,r-width))),max(t,min(y,max(t,b-height))))


def place(window,x,y,width=None,height=None):
    window.update_idletasks()
    x,y=clamp_rect(x,y,width or window.winfo_width(),height or window.winfo_height(),work_areas(window))
    # '+-1920' is an absolute negative coordinate in Tk, unlike '-1920'.
    window.geometry(f'+{int(x)}+{int(y)}')
    return x,y
