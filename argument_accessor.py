"""
Project specific accessor for command line arguments.
"""
import argparse
import sys
from pathlib import Path
from typing import Optional
from standalone.arg_casting import cast as cast_arg

_self = sys.modules[__name__]


# =================================================================================================
# region Variables

project_root: Path
godot_version: str
export_preset: str
export_path: Path
debug: bool = False
compile_options: dict = {}
encryption_key: Optional[str]

_arg_kwargs = {
	"project_root": {
		"help": "Path to the project root folder."
	},
	"godot-version": {
		"help": "Godot version to use (e.g. 4.6)."
	},
	"export-preset": {
		"help": "Export preset name defined in the project."
	},
	"export-path": {
		"help": "Where to export the project to."
	},
	"--debug": {
		"help": "Produce a debug export instead of a signed release export.",
		"action": "store_true"
	},
	"--compile-options": {
		"help": "Comma-separated template compile options (e.g. javascript_eval=no,threads=no).",
	},
	"--encryption-key": {
		"help": "64bit hex key to encrypt template and export with.",
		"default": None,
		"_sensitive": True
	}
}
# =================================================================================================


def _load_args():
	parser = argparse.ArgumentParser(
		description="Wrap the build process for compiling templates and exporting a Godot project."
	)

	for arg_name, metadata in _arg_kwargs.items():
		kwargs = {key: value for key, value in metadata.items() if not key.startswith("_")}
		parser.add_argument(arg_name, **kwargs)

	args, _unknown = parser.parse_known_args()
	for name, value in vars(args).items():
		_parse_arg(name, value)


def _parse_arg(name: str, value: object):
	name = name.replace("-", "_")
	var_type = __annotations__[name]
	casted_value = cast_arg(value, var_type)
	setattr(_self, name, casted_value)


# def _set_sensitive_in_logger():
# 	from standalone import logger
# 	for name, metadata in _arg_kwargs.items():
# 		if metadata.get("_sensitive", False):
# 			attribute_name = name.removeprefix("--").replace("-", "_")
# 			logger.hide.add(getattr(_self, attribute_name))


def _print_args():
	print("\nCommand line args ".ljust(100, "="))

	raw_names = list(_arg_kwargs.keys())
	names = [name.removeprefix("--").replace("-", "_") for name in raw_names]
	values = [getattr(_self, names[i]) if not _arg_kwargs[raw_names[i]].get("_sensitive", False) else "[redacted]" for i in range(len(raw_names)) ]
	types = [type(value).__name__ for value in values]

	max_name_length = max([len(names[i]) for i in range(len(names))])
	max_type_length = max([len(types[i]) for i in range(len(names))])
	max_value_length = max([len(str(values[i])) for i in range(len(names))])

	for i in range(len(names)):
		name = names[i].ljust(max_name_length)
		var_type = types[i]#.ljust(max_type_length)
		value = str(values[i]).ljust(max_value_length)
		print(f"{name} = {value} ({var_type})")

	print("\n".rjust(100, "="))


_load_args()
# _set_sensitive_in_logger()
# _print_args()
