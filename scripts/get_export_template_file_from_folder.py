"""Helpers for locating platform-specific export templates in a folder."""
from pathlib import Path


class _ExportTemplateFinder:
	"""Locate a single export template file for a given platform."""
	def __init__(self, folder: Path):
		"""Create a finder scoped to a template output folder."""
		self.folder = folder

	def get_template(self, platform: str) -> Path:
		"""Return the first matching template file for the platform."""
		match platform.lower():
			case "web":
				return self._find_first_of_type(".zip")
			case "windows":
				return self._find_first_of_type(".exe")
		print(
			f"WARNING: No finder for platform {platform} implemented! Returning folder path...")
		return self.folder

	def _find_first_of_type(self, extension: str) -> Path:
		"""Find the first file in the folder with the given extension."""
		for item in self.folder.iterdir():
			if item.suffix == extension:
				return item
		raise FileNotFoundError(
			f"Could not find a {extension} file in {self.folder.resolve()}!")


def get_export_template_file_from_folder(platform: str, folder: Path) -> Path:
	"""Convenience wrapper to locate a template file by platform."""
	return _ExportTemplateFinder(folder).get_template(platform)
