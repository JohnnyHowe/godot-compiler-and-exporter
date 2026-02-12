import os
from pathlib import Path
import shlex
import subprocess
from typing import Optional


ENCRYPTION_KEY_KEY = "SCRIPT_AES256_ENCRYPTION_KEY"


def export(
	project_root: Path,
	debug: bool,
	preset_name: str,
	export_path: Path,
	log_prefix="",
	encryption_key: Optional[str] = None
):
	"""
	Wraps `godot --headless --export...`.
	See https://docs.godotengine.org/en/latest/tutorials/editor/command_line_tutorial.html
	"""

	command = [
		"godot", "--headless",
		"--path", _sanitise_path(project_root),
		"--export-debug" if debug else "--export-release", preset_name, _sanitise_path(export_path)
	]

	print(log_prefix + shlex.join(command))

	env = os.environ.copy()
	if encryption_key != None:
		env[ENCRYPTION_KEY_KEY] = encryption_key
	else:
		env.pop(ENCRYPTION_KEY_KEY)		# Ensure it's not there

	with subprocess.Popen(command, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as process:
		for line in process.stdout:
			print(log_prefix + line, end="")


def _sanitise_path(path: Path) -> str:
	return str(path.resolve()).replace("\\\\", "/").replace("\\", "/")


# TODO run from command line args