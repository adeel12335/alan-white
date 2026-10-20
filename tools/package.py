"""Create production and editable source ZIPs from the completed build."""
from pathlib import Path
import zipfile
ROOT=Path(__file__).resolve().parent.parent
for label,source in [('production',ROOT/'dist'),('source',ROOT)]:
    output=ROOT.parent/f'structural-systematic-{label}.zip'
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as archive:
        for p in source.rglob('*'):
            if p.is_file() and not any(x in p.relative_to(source).parts for x in ['.git','source-images','__pycache__']):
                archive.write(p,p.relative_to(source))
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None
        for required in ['premium.css','showcase.css','showcase.js','assets/documents/alan-white-cv.pdf']:
            assert required in archive.namelist()
    print(f'{output.name}: verified ({output.stat().st_size:,} bytes)')
