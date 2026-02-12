from enum import Enum
import os
from pathlib import Path
import queue
import shlex
import subprocess
import threading
from typing import Iterable
from .pretty_print import *


class OutputSource(Enum):
	STDOUT = 0
	STDERR = 1
	OTHER = 2

	def __str__(self):
		return self.name


LOG_COLORS = {
	OutputSource.STDERR: Colors.ERROR,
}

class OutputLine:
	source: OutputSource
	test: str

	def __init__(self, text: str, source: OutputSource = OutputSource.OTHER) -> None:
		self.text = text
		self.source = source

	def __repr__(self):
		return str(self)

	def __str__(self):
		return f"[{str(self.source)}] {self.text}"

	def __iter__(self):
		yield self.text
		yield self.source


def run_command_and_print_lines(*args, log_colors: dict = LOG_COLORS, std_prefix: str = "", **kwargs) -> Iterable[OutputLine]:
	"""	Wraps subprocess.Popen. Printing and yielding every output line. """
	kwargs["cwd"] = str(Path(kwargs.get("cwd", os.getcwd())).resolve())

	print("> " + shlex.join(args[0]))
	print(f"(cwd={kwargs["cwd"]})")

	for line in run_command(*args, **kwargs):
		pretty_print(
			std_prefix + str(line),
			color=log_colors.get(line.source, Colors.REGULAR)
		)
		yield line


def run_command(*args, **kwargs) -> Iterable[OutputLine]:
	""" Wraps subprocess.Popen yielding every output line as an OutputLine object. """

	kwargs["stdout"] = subprocess.PIPE
	kwargs["stderr"] = subprocess.PIPE
	kwargs["text"] = True

	cwd = str(Path(kwargs.pop("cwd", os.getcwd())).resolve())
	with subprocess.Popen(*args, cwd=cwd, **kwargs) as process:

		out_queue: "queue.Queue[OutputLine]" = queue.Queue()

		def _drain(stream, source_type: OutputSource):
			if not stream:
				return
			for line in stream:
				out_queue.put(OutputLine(line.removesuffix("\n"), source_type))

		threads = [
			threading.Thread(target=_drain, args=(process.stdout, OutputSource.STDOUT), daemon=True),
			threading.Thread(target=_drain, args=(process.stderr, OutputSource.STDERR), daemon=True),
		]
		for thread in threads:
			thread.start()

		while True:
			try:
				yield out_queue.get(timeout=0.05)
			except queue.Empty:
				if process.poll() is not None and all(not t.is_alive() for t in threads):
					break


def evaluate_iterable(iterable: Iterable):
	for _ in iterable:
		pass
