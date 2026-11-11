import tempfile
from pathlib import Path
from desktop_runtime import read_settings, write_settings
with tempfile.TemporaryDirectory() as d:
    p=Path(d)/'settings.json'
    assert read_settings(p)=={}
    write_settings({'size':360,'x':123,'y':234,'auto_sleep':False},p)
    assert read_settings(p)=={'size':360,'x':123,'y':234,'auto_sleep':False}
    p.write_text('{broken',encoding='utf-8')
    assert read_settings(p)=={}
    p.write_text('[]',encoding='utf-8')
    assert read_settings(p)=={}
print('PASS: settings roundtrip, missing and damaged files')
