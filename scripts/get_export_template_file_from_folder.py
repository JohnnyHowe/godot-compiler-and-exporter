"""Helpers for locating platform-specific export templates in a folder."""
from pathlib import Path
from typing import Iterable


class _ExportTemplateFinder:
	"""Locate a single export template file for a given platform."""
	def __init__(self, folder: Path):
		"""Create a finder scoped to a template output folder."""
		self.folder = folder

	def get_template(self, platform: str) -> Path:
		"""Return the first matching template file for the platform."""
		match platform.lower():
			case "web":
				return self._find_of_type(".zip")
			case "windows":
				return self._find_of_type(".exe")
		print(
			f"WARNING: No finder for platform {platform} implemented! Returning folder path...")
		return self.folder

	def _find_of_type(self, extension: str) -> Path:
		"""Find the first file in the folder with the given extension."""
		options = list(self._find_all_of_type(extension))

		# uh, oh
		if len(options) == 0:
			raise FileNotFoundError(
				f"Could not find a {extension} file in {self.folder.resolve()}!")

		# just one, very good
		if len(options) == 1:
			return options[0]

		# console in one?
		non_console_items = [path for path in options if not path.stem.endswith(".console")]
		if len(non_console_items) == 1:
			return non_console_items[0]

		print("Could not decide what file export template is!")
		print(f"\tFound {', '.join(options)}")
		chosen = non_console_items[0]
		print(f"\Taking first: {chosen}")
		return chosen


	def _find_all_of_type(self, extension: str) -> Iterable[Path]:
		for item in self.folder.iterdir():
			if item.suffix == extension:
				yield item


def get_export_template_file_from_folder(platform: str, folder: Path) -> Path:
	"""Convenience wrapper to locate a template file by platform."""
	return _ExportTemplateFinder(folder).get_template(platform)
