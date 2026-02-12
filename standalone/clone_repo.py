from pathlib import Path
import subprocess


def clone_if_required(path: Path, url: str) -> None:
	command = [
		"git", "clone",
		url,
		"--depth", "1",
		str(path.resolve())
	]

	print(f"Attemping to clone {url} into {str(path.resolve())}...")
	with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as process:
		for line in process.stdout:
			print("  - " + line, end="")
	pull(path)


def pull(path: Path) -> None:
	print(f"Attemping to pull in {str(path.resolve())}...")
	with subprocess.Popen(["git", "pull"], cwd=path.resolve(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as process:
		for line in process.stdout:
			print("  - " + line, end="")