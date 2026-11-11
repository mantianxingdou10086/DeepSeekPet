from motion_timing import typing_pose
assert typing_pose(.22)==2, 'third local typing pose not scheduled'
from motion_timing import wakeup_pose, WAKE_DURATION
assert wakeup_pose(0)==0
assert wakeup_pose(.3)==1
assert wakeup_pose(.7)==0
assert wakeup_pose(1.0)==1
assert wakeup_pose(1.6)==2
assert wakeup_pose(WAKE_DURATION-.1)==6
print('PASS three typing poses and wake blink/sit/settle timing')
