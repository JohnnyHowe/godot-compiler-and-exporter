from pathlib import Path
import argument_accessor
import constants

from standalone.clone_repo import clone_if_required as clone_repo
from standalone.export_project import export
from standalone import export_preset_access
from standalone.sanitise_path import sanitise_path

from template_builder import build_template


def _main():
	clone_repo(
		constants.TEMPLATE_CREATOR_PATH,
		constants.TEMPLATE_CREATOR_URL
	)

	print()

	preset_accessor = export_preset_access.ExportPresetAccessor(argument_accessor.project_root / constants.EXPORT_PRESETS_FILENAME)
	preset = preset_accessor.get_preset(argument_accessor.export_preset)

	template_path = build_template(preset["platform"])

	modify_preset(preset, template_path)
	preset_accessor.save()

	print()

	export(
		argument_accessor.project_root,
		argument_accessor.debug,
		argument_accessor.export_preset,
		argument_accessor.export_path,
		argument_accessor.encryption_key
	)


def modify_preset(preset: dict, template_path: Path):
	encrypted = argument_accessor.encryption_key == None
	preset["encrypt_pck"] = encrypted
	preset["encrypt_directory"] = encrypted

	preset["options"]["custom_template/release"] = sanitise_path(template_path)
	preset["options"]["custom_template/debug"] = sanitise_path(template_path)

	export_path = argument_accessor.export_path
	export_path.parent.mkdir(parents=True, exist_ok=True)

	preset["export_path"] = sanitise_path(export_path)
			


if __name__ == "__main__":
	_main()