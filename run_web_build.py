import argparse
from pathlib import Path
import subprocess

import constants


parser = argparse.ArgumentParser()
parser.add_argument("export_root", type=Path)
args = parser.parse_args()

export_root = args.export_root

runner = constants.TEMPLATE_CREATOR_PATH / "godot-source" / "4.6" / "platform/web/serve.py"

subprocess.run(["python", runner, "-r", str(export_root.resolve())])

