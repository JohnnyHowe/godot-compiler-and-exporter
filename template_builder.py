from pathlib import Path
import shlex
import subprocess
import constants
import argument_accessor

from export_preset_accessor import preset_accessor
from standalone.get_export_template_file_from_folder import get_export_template_file_from_folder


LOG_HEADER = ""


def build_template(platform: str) -> Path:
	print("Building template ...")
	command = _build_command()

	print(f"Running the following command in {constants.TEMPLATE_CREATOR_PATH}")

	with subprocess.Popen(command, cwd=constants.TEMPLATE_CREATOR_PATH, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as process:
		for line in process.stdout:
			print(LOG_HEADER + line, end="")

	# Last line of log is the output folder
	output_folder = Path(line.strip()).resolve()
	return get_export_template_file_from_folder(platform, output_folder)
	

def _build_command() -> list[str]:
	return [
		"python", "run.py",
		"--env-overrides", _get_env_overrides_arg()
	]


def _get_env_overrides_arg() -> str:
	env_overrides = {
		"GODOT_VERSION": argument_accessor.godot_version,
		"COMPILE_OPTIONS": f"[{_as_arg(_get_compile_options())}]",
		"OUTPUT_FOLDER": str(constants.TEMPLATES_PATH)
	}
	if argument_accessor.encryption_key.strip():
		env_overrides["SCRIPT_AES256_ENCRYPTION_KEY"] = argument_accessor.encryption_key
	return _as_arg(env_overrides)


def _get_compile_options() -> dict:
	return {
		"platform": preset_accessor.get_preset(argument_accessor.export_preset)["platform"].lower(),
		"target": "template_debug" if argument_accessor.debug else "template_release",
	}


def _as_arg(items: dict) -> str:
	parts = []
	for key, value in items.items():
		parts.append(f"{key}={value}")
	return ",".join(parts)
