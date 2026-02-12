from . import cfg_parser
from pathlib import Path


OPTIONS_KEY = "options"

class ExportPresetAccessor:
	file_path: Path
	_presets: dict
	_reader: cfg_parser.Reader
	_names: list[str]

	def __init__(self, file_path: Path) -> None:
		self.file_path = file_path
		self.reload()

	def reload(self):
		self._reader = cfg_parser.Reader(self.file_path)
		self._load_preset_names()

		self._presets = {}

		presets_by_names = {self._get_preset_name_from_header(header): data for header, data in self._reader.blocks.items() if not "options" in header}
		options_by_names = {self._get_preset_name_from_header(header): data for header, data in self._reader.blocks.items() if "options" in header}

		for name, data in options_by_names.items():
			presets_by_names[name][OPTIONS_KEY] = data

		self._presets = presets_by_names

	def _get_preset_name_from_header(self, header: str) -> str:
		return self._names[ExportPresetAccessor._get_index_from_header(header)]

	def _load_preset_names(self) -> None:
		self._names = []
		for header, data in self._reader.blocks.items():
			if "options" in header:
				continue

			index = ExportPresetAccessor._get_index_from_header(header)
			while index >= len(self._names):
				self._names.append(None)
			self._names[index] = data["name"]

	@staticmethod
	def _get_index_from_header(header: str) -> int:
		number_str = header.removeprefix("[preset.").removesuffix("]").removesuffix(".options")
		return int(number_str)

	def get_preset(self, name: str) -> dict:
		""" Returns a REFERENCE to the preset"""
		return self._presets[name]

	def set_preset(self, data: dict):
		self._presets[data["name"]] = data

	def save(self) -> None:
		blocks = {}
		for preset in self._presets.values():
			self._add_presets_as_blocks(preset, blocks)
		self._save_cgf_blocks(blocks)

	@staticmethod
	def _add_presets_as_blocks(preset_data: dict, blocks: dict):
		preset_data_copy = preset_data.copy()
		options = preset_data_copy.pop(OPTIONS_KEY)

		blocks[preset_data[cfg_parser.HEADER_KEY]] = preset_data_copy
		blocks[options[cfg_parser.HEADER_KEY]] = options

	def _save_cgf_blocks(self, blocks: dict):
		cfg_parser.Saver(blocks).save_as_cfg(self.file_path)