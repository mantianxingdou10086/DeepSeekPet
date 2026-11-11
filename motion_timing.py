# 用独立动作时钟，避免共用64帧索引导致短动作循环截断。
def typing_pose(elapsed):
    phase=elapsed%2.4
    for start,end in ((.09,.18),(.31,.40),(.52,.60),(.83,.94)):
        if start<=phase<end:return 1
    for start,end in ((.21,.29),(.43,.50),(.64,.73),(.98,1.08)):
        if start<=phase<end:return 2
    return 0

WAKE_DURATION = 3.4
WAKE_FRAME_COUNT = 17

def wakeup_pose(elapsed):
    """Semantic phases: blink, sit, knee, cover, reveal, exact idle."""
    if elapsed < .18:return 0
    if elapsed < .62:return 1
    if elapsed < .76:return 0
    if elapsed < 1.18:return 1
    if elapsed < 1.85:return 2
    if elapsed < 2.50:return 3
    if elapsed < 2.74:return 4
    if elapsed < 2.98:return 5
    return 6

def wakeup_frame(elapsed):
    phase = wakeup_pose(elapsed)
    if phase < 4:
        return phase
    if elapsed < 2.98:
        return min(15, 4 + int(round((elapsed - 2.50) * 1000) // 40))
    return 16

def rice_pose(elapsed):
    # Scoop, lift, taste, then a quiet chewing hold. No full-body motion.
    phase = max(0, elapsed) % 3.2
    if phase < .7: return 0
    if phase < 1.0: return 1
    if phase < 1.8: return 2
    if phase < 2.1: return 1
    return 0

def sleep_frame(elapsed):
    return int(round(max(0,elapsed)*1000)//130)%24
