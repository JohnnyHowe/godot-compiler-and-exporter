import re
#import argument_accessor
from pathlib import Path


FEATURES_REGEX = re.compile(r"config\/features=[A-z]*\((.*)\)")


def get_project_version() -> str:
    for feature in _get_features():
        try:
            stripped = feature.replace("\"", "").replace("'", "")
            float(stripped) # ensure it can be 
            return stripped
        except:
            pass


def _get_features() -> list[str]:
    match = FEATURES_REGEX.search(_get_file_contents())
    if not match:
        raise KeyError("Could not find config/features in project.godot!")
    return match.group(1).split(", ")


def _get_file_contents() -> str:
    with open(_get_project_file_path(), "r") as file:
        contents = file.read()
    return contents


def _get_project_file_path() -> Path:
    #return argument_accessor.project_root / "project.godot"
    return Path("C:/Users/Work/Documents/Projects/dwarfhold/project.godot")


print(get_project_version())