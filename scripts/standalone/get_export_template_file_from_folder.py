from pathlib import Path


class _ExportTemplateFinder:
	def __init__(self, folder: Path):
		self.folder = folder

	def get_template(self, platform: str) -> Path:
		match platform.lower():
			case "web":
				return self._find_first_of_type(".zip")
		print(f"WARNING: No finder for platform {platform} implemented! Returning folder path...")
		return self.folder

	def _find_first_of_type(self, extension: str) -> Path:
		for item in self.folder.iterdir():
			if item.suffix == extension:
				return item
		raise FileNotFoundError(f"Could not find a {extension} file in {self.folder}!")


def get_export_template_file_from_folder(platform: str, folder: Path) -> Path:
	return _ExportTemplateFinder(folder).get_template(platform)