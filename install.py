"""Download required libs/files. Sorry, I'm not a fan of mpremote/mip solution"""
import urllib.request
from pathlib import Path
import glob
import os


files = glob.glob('./lib/**/*', recursive=True)

for f in files:
    try:
        if Path(f).is_file:
            os.remove(f)
        else:
            os.rmdir(f)
    except OSError as e:
        print("Error: %s : %s" % (f, e.strerror))


hcsr04sensor = "./lib"
Path(hcsr04sensor).mkdir(parents=True, exist_ok=True)
urllib.request.urlretrieve('https://raw.githubusercontent.com/rsc1975/micropython-hcsr04/master/hcsr04.py', './lib/hcsr04.py')
