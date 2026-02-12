from pathlib import Path


def sanitise_path(path: Path) -> str:
	return str(path.resolve()).replace("\\\\", "/").replace("\\", "/")
