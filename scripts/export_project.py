from pathlib import Path
from typing import Optional

from .standalone.template_builder import build_template
from .standalone.preset_exporting import export_modified_preset
import constants


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

    # Build template
    template_path = build_template(
        constants.TEMPLATES_PATH,
        godot_version,
        platform,
        all_compile_options,
        encryption_key,
    )

    debug = False  # TODO

	# Build preset overrides
    encrypted = encryption_key is not None
    full_template_path = str(template_path.resolve())
    preset_overrides = {
        "encrypt_pck": encrypted,
        "encrypt_directory": encrypted,

        "export_path": str(export_path),

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
