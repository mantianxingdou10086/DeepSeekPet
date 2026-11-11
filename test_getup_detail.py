"""Real supported-knee pose + explicitly stylized short water-puff handoff."""
from pathlib import Path
from PIL import Image
from motion_timing import wakeup_pose, WAKE_DURATION
visited=[]
for tick in range(round(WAKE_DURATION*100)):
    p=wakeup_pose(tick/100)
    if not visited or visited[-1]!=p: visited.append(p)
assert visited==[0,1,0,1,2,3,4,5,6],visited
assert wakeup_pose(-1)==0
assert wakeup_pose(WAKE_DURATION+10)==6
from motion_timing import wakeup_frame
root=Path(__file__).parent
frames=[Image.open(root/'assets/wakeup'/f'{i:02d}.png').convert('RGBA') for i in range(17)]
assert all(f.size==(400,420) for f in frames)
assert frames[3].getbbox()[3]==400,frames[3].getbbox()
assert frames[-1].tobytes()==Image.open(root/'assets/layered/00.png').convert('RGBA').tobytes()
assert wakeup_frame(WAKE_DURATION)==16
assert len({wakeup_frame(t/1000) for t in range(round(WAKE_DURATION*1000))})==17
assert frames[3].tobytes()!=frames[2].tobytes()
# Full occlusion at swap: no double face or exposed silhouette discontinuity.
assert frames[9].tobytes()==frames[10].tobytes()
print('PASS 17 frames; real knee pose; short opaque handoff; exact idle; safe boundaries')
