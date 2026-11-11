import tkinter as tk
from types import SimpleNamespace
from unittest.mock import patch
from pet import Pet

r=tk.Tk(); p=Pet(r); r.update()
try:
    p.start=(0,0,100,100)
    p.drag(SimpleNamespace(x_root=99999,y_root=99999));r.update()
    assert r.winfo_x()+r.winfo_width() <= r.winfo_screenwidth(), 'drag escaped right edge'
    assert r.winfo_y()+r.winfo_height() <= r.winfo_screenheight(), 'drag escaped bottom edge'
    from window_bounds import clamp_rect
    areas=[(-1920,0,0,1040),(0,0,1920,1040)]
    assert clamp_rect(-1800,900,360,378,areas)==(-1800,662)
    assert clamp_rect(1900,1000,360,378,areas)==(1560,662)
    assert clamp_rect(-1800,900,360,378,[(0,0,1920,1040)])==(0,662)
    with patch('window_bounds.work_areas',return_value=[(0,0,800,600)]):
        r.geometry('+590+370');r.update();p.load_size(360);r.update()
        assert (r.winfo_x(),r.winfo_y())==(440,222)
        r.geometry('+3000+3000');r.update();p.ensure_visible();r.update()
        assert (r.winfo_x(),r.winfo_y())==(440,222)
    print('PASS dragging, resizing, negative-monitor coordinates, monitor removal recovery')
finally:p.quit()
