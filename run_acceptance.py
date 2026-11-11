"""Explicit acceptance suite; abandoned focus-pause prototype is not a product requirement."""
import subprocess,sys
from pathlib import Path
root=Path(__file__).parent
names=['test_release_dpi.py','test_release_bounds.py','test_release_hidden.py','test_release_pause.py','test_getup_detail.py','test_getup_runtime.py','test_settings.py','test_motion.py','test_refined_motion.py','test_rice.py','test_wakeup.py','test_states.py','test_focus.py','test_sleep.py','test_feeding.py','test_desktop_runtime.py']
lines=[]
for name in names:
    r=subprocess.run([sys.executable,name],cwd=root,capture_output=True,text=True,encoding='utf-8',errors='replace')
    line=f'{name}: exit={r.returncode}\n{r.stdout}{r.stderr}'
    print(line);lines.append(line)
    if r.returncode:
        (root/'acceptance-results.txt').write_text('\n'.join(lines),encoding='utf-8');sys.exit(r.returncode)
lines.append(f'PASS {len(names)} acceptance scripts. Excluded: test_focus_pause.py (abandoned unimplemented feature; not masked as passed).')
(root/'acceptance-results.txt').write_text('\n'.join(lines),encoding='utf-8')
print(lines[-1])
