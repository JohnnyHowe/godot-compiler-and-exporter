import shlex
import subprocess

from typing import Optional
from pathlib import Path


TEMPLATE_CREATOR_PATH = Path("./godot-template-creator").resolve()


def build_template(
	output_folder: Path,
	godot_version: str,
	platform: str,
	compile_options: dict,
	encryption_key: Optional[str],
) -> Path:
	"""
	Build a Godot export template using the template creator and return the template file.
	Wraps godot-template-creator tool. See https://github.com/JohnnyHowe/godot-template-creator

	Args:
		template_creator_path: Path to the godot-template-creator repository.
		templates_path: Output folder for compiled templates.
		godot_version: Godot version to build templates for (e.g. "4.6").
		export_preset_data: Export preset data containing the platform information.
		compile_options: Optional additional compile options to pass to the template creator.
		encryption_key: Optional encryption key to embed in the template.

	Returns:
		Path to the exported template file for the preset's platform.
	"""
	print("Building template ...")

	all_compile_options = compile_options.copy()
	all_compile_options["platform"] = platform

	compile_options_key_value_strings = [f"{key}={str(value)}" for key, value in all_compile_options.items()]
	compile_options_list_with_key = [item for key_value in compile_options_key_value_strings for item in ("--compile-option", key_value)]

	command =  [
		"python", "-u", "create_template.py", godot_version, str(output_folder.resolve()),
		*compile_options_list_with_key,
	]

	if encryption_key:
		command += ["--encryption-key", encryption_key]

	print(f"Running the following command in {TEMPLATE_CREATOR_PATH}")
	print(shlex.join(command))

	with subprocess.Popen(
		command,
		cwd=TEMPLATE_CREATOR_PATH,
		stdout=subprocess.PIPE,
		stderr=subprocess.STDOUT,
		text=True
	) as process:
		for line in process.stdout:
			print(line, end="")

	# Last line of log is the template file
	return Path(line.strip()).resolve()
