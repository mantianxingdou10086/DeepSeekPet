import tkinter as tk
from pathlib import Path
import json
import sys
import time
import random
import math
from PIL import Image, ImageTk, ImageDraw, ImageFont
from window_bounds import place
from motion_timing import typing_pose, sleep_frame, rice_pose, wakeup_frame, WAKE_DURATION, WAKE_FRAME_COUNT

ROOT = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))

class Pet:
    def __init__(self, root):
        self.root = root
        self.size = 280
        self.paused = False
        self.index = 0
        self.motion_clock = 0.0
        self.motion_last = time.monotonic()
        self.sequence = list(range(64))
        self.delays = [70] * 64
        self.dragged = False
        self.after_id = None
        self.bubble_id = None
        self.pending_reminder = None
        root.title('DeepSeek 桌宠')
        root.overrideredirect(True)
        root.configure(bg='#ff00ff')
        root.attributes('-transparentcolor', '#ff00ff')
        root.attributes('-topmost', True)
        self.label = tk.Label(root, bg='#ff00ff', bd=0, highlightthickness=0)
        self.label.pack()
        self.happy_until = 0
        self.feed_started = None
        self.rice_started = None
        self.restore_sleep_after_rice = False
        self.feed_times = []
        self.feed_consumed = False
        self.feed_finished = 0
        self.sleeping = False
        self.focus_deadline = None
        self.focus_window = None
        self.focus_label = None
        self.focus_stamp = None
        self.sleep_started = 0
        self.last_interaction = time.monotonic()
        self.auto_sleep = True
        self.sleep_font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 24)
        self.originals = [Image.open(ROOT/'assets'/'layered'/f'{i:02d}.png').convert('RGBA') for i in range(64)]
        self.happy_originals = [Image.open(ROOT/'assets'/'happy'/f'{i:02d}.png').convert('RGBA') for i in range(64)]
        self.restore_sleep_after_feed = False
        self.waking_until = 0
        self.wakeup_originals = [Image.open(ROOT/'assets'/'wakeup'/f'{i:02d}.png').convert('RGBA') for i in range(WAKE_FRAME_COUNT)]
        self.typing_originals = [Image.open(ROOT/'assets'/'typing'/f'{i:02d}.png').convert('RGBA') for i in range(3)]
        self.prone_originals = [Image.open(ROOT/'assets'/'prone'/f'{i:02d}.png').convert('RGBA') for i in range(24)]
        self.rice_originals = [Image.open(ROOT/'assets'/'rice'/f'{i:02d}.png').convert('RGBA') for i in range(3)]
        self.load_size(self.size)
        root.geometry(f'+{root.winfo_screenwidth()-self.size-55}+{root.winfo_screenheight()-self.size-100}')
        self.label.bind('<ButtonPress-1>', self.press)
        self.label.bind('<B1-Motion>', self.drag)
        self.label.bind('<ButtonRelease-1>', self.release)
        self.label.bind('<Button-3>', self.menu)
        root.bind('<Escape>', lambda e: self.quit())
        self.bubble = None
        self.animate()

    def load_size(self, size):
        self.size = size
        self.frames = []
        self.happy_frames = []
        for number, original in enumerate(self.originals + self.happy_originals):
            im = original.resize((size, round(size*420/400)), Image.Resampling.LANCZOS)
            # Windows 色键透明只认精确颜色，不能保留会混入粉底的半透明边缘。
            alpha = im.getchannel('A').point(lambda a: 255 if a >= 128 else 0)
            im.putalpha(alpha)
            (self.frames if number < 64 else self.happy_frames).append(ImageTk.PhotoImage(im))
        self.typing_frames = []
        self.prone_frames = []
        self.wakeup_frames = []
        self.rice_frames = []
        for originals, target in [(self.typing_originals,self.typing_frames),(self.prone_originals,self.prone_frames),(self.wakeup_originals,self.wakeup_frames),(self.rice_originals,self.rice_frames)]:
            for original in originals:
                im = original.resize((size,round(size*420/400)),Image.Resampling.LANCZOS)
                im.putalpha(im.getchannel('A').point(lambda a:255 if a>=128 else 0))
                target.append(ImageTk.PhotoImage(im))
        self.label.configure(image=self.frames[self.sequence[self.index]])
        self.ensure_visible()

    def ensure_visible(self):
        place(self.root,self.root.winfo_x(),self.root.winfo_y(),self.size,round(self.size*1.05))

    def visual_state(self):
        if self.rice_started is not None:
            return 'eating'
        if self.feed_started is not None:
            return 'feeding'
        if self.sleeping:
            return 'sleeping'
        if self.focus_deadline is not None:
            return 'typing'
        if time.monotonic() < self.waking_until:
            return 'waking'
        return 'idle'

    def advance_clock(self, now):
        elapsed = max(0,now-self.motion_last)
        if self.paused:
            for name in ('feed_started','rice_started','waking_until','happy_until'):
                value=getattr(self,name)
                if value is not None and value > 0:setattr(self,name,value+elapsed)
        else:
            self.motion_clock += elapsed
        self.motion_last = now

    def animate(self):
        now = time.monotonic()
        self.advance_clock(now)
        self.update_focus(now)
        if self.paused:
            self.after_id = self.root.after(200,self.animate)
            return
        if self.auto_sleep and self.focus_deadline is None and not self.paused and not self.sleeping and self.feed_started is None and self.rice_started is None and now-self.last_interaction >= 300:
            self.sleep()
        active_frames = self.happy_frames if time.monotonic() < self.happy_until else self.frames
        if self.rice_started is not None:
            elapsed = now-self.rice_started
            self.label.configure(image=self.rice_frames[rice_pose(elapsed)])
            if elapsed >= 6.4:
                self.rice_started = None
                self.last_interaction = now
                if self.restore_sleep_after_rice:
                    self.restore_sleep_after_rice = False
                    self.sleep()
        elif self.feed_started is not None:
            elapsed = time.monotonic() - self.feed_started
            if elapsed >= 0.8 and not self.feed_consumed:
                self.feed_consumed = True
                self.feed_finished += 1
                self.happy_until = time.monotonic() + 1.7
                self.say('吃饱啦，陪你学习一会儿！' if len(self.feed_times) >= 3 else '好吃！还能再来一颗吗～')
            image = self.render_feed(elapsed)
            self.effect_photo = ImageTk.PhotoImage(image)
            self.label.configure(image=self.effect_photo)
            if elapsed >= 2.2:
                self.feed_started = None
                if self.restore_sleep_after_feed:
                    self.restore_sleep_after_feed = False
                    self.sleep()
        elif self.sleeping:
            self.label.configure(image=self.prone_frames[sleep_frame(self.motion_clock)])
        elif self.focus_deadline is not None:
            self.label.configure(image=self.typing_frames[typing_pose(self.motion_clock)])
        elif now < self.waking_until:
            frame = wakeup_frame(WAKE_DURATION-(self.waking_until-now))
            self.label.configure(image=self.wakeup_frames[frame])
        else:
            self.label.configure(image=active_frames[self.sequence[self.index]])
        delay = 40 if self.rice_started is not None or now < self.waking_until or self.feed_started is not None or self.focus_deadline is not None or self.sleeping else self.delays[self.index]
        if not self.paused:
            self.index = (self.index+1) % len(self.sequence)
        self.after_id = self.root.after(delay if not self.paused else 200, self.animate)

    def start_focus(self, minutes=25):
        self.stop_focus()
        self.wake()
        self.focus_deadline = time.monotonic()+minutes*60
        self.focus_window = tk.Toplevel(self.root)
        self.focus_window.overrideredirect(True)
        self.focus_window.attributes('-topmost', True)
        self.focus_label = tk.Label(self.focus_window, font=('Microsoft YaHei UI', 10), bg='#e7f1ff', fg='#254775', padx=12, pady=7, bd=1, relief='solid')
        self.focus_label.pack()
        self.focus_label.bind('<Button-3>', self.menu)
        self.focus_stamp = None
        self.update_focus(time.monotonic())
        self.say('开始专注啦，我陪你一起！')

    def stop_focus(self):
        self.focus_deadline = None
        if self.focus_window is not None:
            self.focus_window.destroy()
            self.focus_window = None
        self.focus_label = None
        self.focus_stamp = None
        self.last_interaction = time.monotonic()

    def update_focus(self, now):
        if self.focus_deadline is None:
            return
        remaining = max(0, math.ceil(self.focus_deadline-now))
        if remaining == 0:
            self.stop_focus()
            self.happy_until = now+2
            self.say('专注完成！看看远处，喝点水，休息一下～', important=True)
            return
        if self.focus_stamp != remaining:
            self.focus_label.configure(text=f'专注陪伴  {remaining//60:02d}:{remaining%60:02d}')
            self.focus_stamp = remaining
        self.focus_window.update_idletasks()
        place(self.focus_window,self.root.winfo_x()+20,self.root.winfo_y()+self.root.winfo_height()-8)

    def wake(self):
        was_sleeping = self.sleeping
        if was_sleeping:
            self.waking_until = time.monotonic()+WAKE_DURATION
        self.sleeping = False
        self.last_interaction = time.monotonic()
        return was_sleeping

    def sleep(self):
        if self.rice_started is not None:
            self.restore_sleep_after_rice = True
            return
        if self.focus_deadline is not None:
            self.stop_focus()
        if self.feed_started is not None:
            return
        self.sleeping = True
        self.sleep_started = time.monotonic()
        self.happy_until = 0
        self.hide_bubble()

    def toggle_auto_sleep(self):
        self.auto_sleep = not self.auto_sleep
        self.wake()

    def render_sleep(self, elapsed):
        image = self.prone_originals[int(max(0,elapsed)/0.13)%len(self.prone_originals)].copy()
        image = image.resize((self.size,round(self.size*420/400)),Image.Resampling.LANCZOS)
        image.putalpha(image.getchannel('A').point(lambda a:255 if a>=128 else 0))
        return image

    def eat_rice(self):
        if self.rice_started is not None or self.feed_started is not None:
            return
        self.restore_sleep_after_rice = self.sleeping
        self.wake()
        self.waking_until = 0
        self.rice_started = time.monotonic()
        self.hide_bubble()

    def feed(self):
        if self.feed_started is not None or self.rice_started is not None:
            return
        was_sleeping = self.sleeping
        self.wake()
        now = time.monotonic()
        self.feed_times = [t for t in self.feed_times if now-t < 60]
        if len(self.feed_times) >= 3:
            self.say('吃饱啦，先陪你学习一会儿～')
            return
        self.restore_sleep_after_feed = was_sleeping
        self.feed_times.append(now)
        self.feed_consumed = False
        self.feed_started = now
        self.hide_bubble()

    def render_feed(self, elapsed):
        originals = self.happy_originals if elapsed >= 0.8 else self.originals
        image = originals[self.sequence[self.index]].copy()
        draw = ImageDraw.Draw(image)
        if elapsed < 0.8:
            t = max(0, min(1, elapsed/0.8))
            smooth = t*t*(3-2*t)
            x, y = 310-125*smooth, 240-45*math.sin(math.pi*t)-48*smooth
            radius = 13*(1-0.65*t)
            draw.polygon([(x,y-radius),(x+radius,y),(x,y+radius),(x-radius,y)], fill='#52bfff', outline='#21569b', width=2)
            draw.line((x-4,y-4,x+4,y-4),fill='white',width=2)
        elif elapsed < 1.7:
            t = (elapsed-0.8)/0.9
            for j in range(7):
                angle = j*math.tau/7
                distance = 10+42*t
                x = 185+math.cos(angle)*distance
                y = 190+math.sin(angle)*distance-15*t
                r = max(1,5*(1-t))
                draw.polygon([(x,y-r),(x+r*0.35,y-r*0.35),(x+r,y),(x+r*0.35,y+r*0.35),(x,y+r),(x-r*0.35,y+r*0.35),(x-r,y),(x-r*0.35,y-r*0.35)],fill='#ffe19b')
        image = image.resize((self.size,round(self.size*420/400)),Image.Resampling.LANCZOS)
        image.putalpha(image.getchannel('A').point(lambda a:255 if a>=128 else 0))
        return image

    def press(self, event):
        self.woke_on_press = self.wake()
        self.start = (event.x_root, event.y_root, self.root.winfo_x(), self.root.winfo_y())
        self.dragged = False
        self.hide_bubble()

    def drag(self, event):
        x, y, wx, wy = self.start
        dx, dy = event.x_root-x, event.y_root-y
        if abs(dx)+abs(dy) > 5:
            self.dragged = True
        place(self.root,wx+dx,wy+dy,self.size,round(self.size*1.05))

    def release(self, event):
        self.last_interaction = time.monotonic()
        if not self.dragged and getattr(self, 'woke_on_press', False):
            self.woke_on_press = False
            self.say('唔……醒啦！我才没有偷偷摸鱼～')
            return
        if not self.dragged:
            self.happy_until = time.monotonic() + 1.6
            self.say(random.choice(['嘿嘿，摸摸头～', '有你陪着，今天也很开心！', '我可不是大肥鱼，哼～', '收到摸摸！能量补充成功。']))

    def say(self, text, important=False):
        self.hide_bubble()
        if getattr(getattr(self, "desktop", None), "hidden", False):
            if important:self.pending_reminder = text
            return
        self.bubble = tk.Toplevel(self.root)
        self.bubble.overrideredirect(True)
        self.bubble.attributes('-topmost', True)
        tk.Label(self.bubble, text=text, font=('Microsoft YaHei UI', 10), bg='#e7f1ff', fg='#254775', padx=14, pady=10, relief='solid', bd=1).pack()
        self.bubble.update_idletasks()
        place(self.bubble,self.root.winfo_x(),self.root.winfo_y()-45)
        self.bubble_id = self.root.after(3000, self.hide_bubble)

    def hide_bubble(self):
        if self.bubble_id:
            self.root.after_cancel(self.bubble_id)
            self.bubble_id = None
        if self.bubble:
            self.bubble.destroy()
            self.bubble = None

    def menu(self, event):
        self.last_interaction = time.monotonic()
        menu = tk.Menu(self.root, tearoff=False)
        if self.focus_deadline is not None:
            menu.add_command(label='结束本次专注', command=self.stop_focus)
        else:
            focus_menu = tk.Menu(menu, tearoff=False)
            for minutes in (5,25,45):
                focus_menu.add_command(label=f'{minutes} 分钟', command=lambda m=minutes:self.start_focus(m))
            menu.add_cascade(label='专注陪伴', menu=focus_menu)
        menu.add_separator()
        menu.add_command(label='叫醒她' if self.sleeping else '打个盹 Zzz', command=self.wake if self.sleeping else self.sleep)
        menu.add_command(label=('✓ ' if self.auto_sleep else '')+'空闲五分钟自动打盹', command=self.toggle_auto_sleep)
        menu.add_command(label='吃大白饭 🍚', command=self.eat_rice)
        menu.add_command(label='喂一颗 Token ◆', command=self.feed)
        menu.add_separator()
        menu.add_command(label='继续动画' if self.paused else '暂停动画', command=self.toggle_pause)
        sizes = tk.Menu(menu, tearoff=False)
        for size, title in [(200,'小'),(280,'中'),(360,'大')]:
            sizes.add_command(label=title, command=lambda s=size: self.load_size(s))
        menu.add_cascade(label='调整大小', menu=sizes)
        menu.add_separator()
        if getattr(self,'desktop',None):
            menu.add_command(label='隐藏到托盘',command=self.desktop.hide)
        menu.add_command(label='退出桌宠', command=self.quit)
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def toggle_pause(self):
        self.advance_clock(time.monotonic())
        self.paused = not self.paused

    def quit(self):
        if getattr(self,'desktop',None):self.desktop.close()
        self.stop_focus()
        if self.after_id:
            self.root.after_cancel(self.after_id)
        self.hide_bubble()
        self.root.destroy()

if __name__ == '__main__':
    if '--test' not in sys.argv:
        from desktop_runtime import acquire_instance
        instance_handle=acquire_instance()
        if instance_handle is None:sys.exit(0)
    root = tk.Tk()
    app = Pet(root)
    if '--test' in sys.argv:
        root.update()
        assert root.attributes('-topmost')
        assert root.attributes('-transparentcolor') == '#ff00ff'
        app.load_size(200)
        assert app.frames[0].width() == 200
        app.toggle_pause()
        assert app.paused
        app.toggle_pause()
        app.release(None)
        assert app.happy_until > time.monotonic()
        assert len(app.happy_frames) == 64
        app.say('交互测试通过')
        root.update()
        assert app.bubble.winfo_exists()
        app.hide_bubble()
        print(json.dumps({'frames':len(app.frames),'transparency':root.attributes('-transparentcolor'),'topmost':bool(root.attributes('-topmost')),'resize':app.size,'bubble':'passed','pause':'passed'}, ensure_ascii=False))
        app.quit()
    else:
        from desktop_runtime import DesktopRuntime
        app.desktop=DesktopRuntime(app,ROOT)
        root.mainloop()
