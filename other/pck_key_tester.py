import argparse
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("build_root", type=Path)
parser.add_argument("encryption_key")
args = parser.parse_args()

pck_file: Path
for file in args.build_root.iterdir():
    if file.suffix == ".pck":
        pck_file = file
        break


cmd = [
    "godot",
    "--headless",
    "--main-pack", pck_file,
    "--quit",
    "--encryption-key", args.encryption_key,
]

result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode == 0 and "ERROR" not in result.stderr:
    print("Key valid")
else:
    print("Key invalid")
    print(result.stderr)
