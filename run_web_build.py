import argparse
from pathlib import Path
import subprocess

import constants


def path_str(path: Path) -> str:
	return str(path.resolve()).replace("\\\\", "/").replace("\\", "/")

parser = argparse.ArgumentParser()
parser.add_argument("export_root", type=Path)
args = parser.parse_args()

export_root = args.export_root

runner = Path("godot-source") / "4.6" / "platform/web/serve.py"

subprocess.run(["python", path_str(runner), "-r", path_str(export_root)])
