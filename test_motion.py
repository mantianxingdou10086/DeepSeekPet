from motion_timing import typing_pose, sleep_frame
assert typing_pose(0)==0
assert typing_pose(.11)==1
assert typing_pose(.20)==0
assert typing_pose(1.4)==0
assert sleep_frame(3.0)==23
assert sleep_frame(3.12)==0
assert sleep_frame(0)==sleep_frame(3.12)
print('PASS: typing burst/pause; all sleep frames; exact cycle boundary')
