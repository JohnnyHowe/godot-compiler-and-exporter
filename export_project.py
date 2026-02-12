"""
Entry point for exporting a Godot project. Parses CLI args and validates
required compile options.
See README.md
"""
import argparse
from pathlib import Path
from typing import Optional

from scripts.generic import argparsing
from scripts.export_project import export_project


def main():
	parser = argparse.ArgumentParser()

	parser.add_argument("project-root", type=Path)
	parser.add_argument("godot-version")
	parser.add_argument("export-preset-name")
	parser.add_argument("export-path", type=Path)

	parser.add_argument("--compile-options", action="append", help="key=value pair")
	parser.add_argument("--encryption-key")

	args, unknown = parser.parse_known_args()

	print(f"Got unknown args: {unknown}")

	argparsing.fix_names(args)
	compile_options: dict = argparsing.arg_to_python(args.compile_options, dict)

	if "target" not in compile_options:
		raise Exception("requires --compile-options target=...")

	project_root: Path = args.project_root.resolve()
	godot_version: str = args.godot_version
	export_preset_name: str = args.export_preset_name
	export_path: Path = args.export_path.resolve()
	encryption_key: Optional[str] = args.encryption_key

	export_project(
		project_root,
		godot_version,
		export_preset_name,
		export_path,
		compile_options,
		encryption_key
	)


if __name__ == "__main__":
	main()




