from pathlib import Path
import subprocess
from typing import Optional

from .godot_custom_preset_exporter import export_modified_preset
import constants

from .godot_template_creator import create_template
from .get_export_template_file_from_folder import get_export_template_file_from_folder


def export_project(
		project_root: Path,
		godot_version: str,
		export_preset_name: str,
		export_path: Path,
		compile_options: dict,
		encryption_key: Optional[str]
) -> None:
	platform = "web"  # TODO

	all_compile_options = compile_options.copy()
	all_compile_options["platform"] = platform

	templates_path = constants.TEMPLATES_PATH

	print("Building template ...")
	template_name = create_template(
		godot_version,
		templates_path,
		all_compile_options,
		encryption_key,
	)
	template_path = get_export_template_file_from_folder(all_compile_options["platform"].lower(), templates_path / template_name)

	debug = False  # TODO

	# Build preset overrides
	encrypted = encryption_key is not None
	full_template_path = template_path.resolve()

	preset_overrides = {
		"encrypt_pck": encrypted,
		"encrypt_directory": encrypted,

		"export_path": export_path,

		"options": {
			"custom_template/release": full_template_path,
			"custom_template/debug": full_template_path,
		}
	}

	# Export modified preset
	export_modified_preset(
		project_root,
		export_preset_name,
		preset_overrides,
		export_path,
		debug,
		encryption_key
	)

	print("Exported project!")
	print(export_path)
	
	# subprocess.run(["python", "run_web_build.py", export_path.parent])
