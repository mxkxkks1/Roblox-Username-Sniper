import subprocess
import sys

libs = [
    "requests",
    "colorama"
]

def install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

for lib in libs:
    install(lib)

print("LMAOOOOO.")
