import argparse
import sys
import zipfile
from zipfile import ZipFile

parser = argparse.ArgumentParser()
parser.add_argument('zipfile')
args = parser.parse_args()

with ZipFile(args.zipfile, 'r') as zin:
    with ZipFile(args.zipfile.replace('.zip', '_fixed.zip'), 'w', zipfile.ZIP_DEFLATED) as zout:
        for i in zin.filelist:
            old = i.filename
            new = old.replace('\\', '/')
            zout.writestr(new, zin.read(i.filename))

sys.stderr.write(zout.filename + '\n')
sys.stderr.flush()
