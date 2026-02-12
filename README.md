Wraps the build process.
1. Compiles new build template (if required) (uses https://github.com/JohnnyHowe/godot-template-creator)
2. exports The project

# TODO
* If cloning or pulling fails, clear clone dir and retry
* Catch and log nice errors from
	* Cloning
	* Pulling
	* Compile command
* Auto detect project godot version (allowing overide via args)
* Ability to clone arbitrary versions (tags or commit hashes?)

# Running
```
python export_project.py <project-root> <godot-version> <export-preset-name> <export-path>
```
Example
```
python export_project.py C:/Users/jon/my_project 4.6 Web \
  C:/Users/jon/my_project/Builds/index.html \
  --compile-options platform=Web \
  --compile-options target=template_debug
```

# Parameters
| Name | Type | Default | Note |
| - | - | - | - |
| `project-root` | `Path` | - | Path to the Godot project. |
| `godot-version` | `string` | - | What version to use. e.g `4.6`.<br>See https://github.com/godotengine/godot/branches for options.
| `export-preset-name` | `string` | - | The name of the export preset set in the project. |
| `export-path` | `Path` | - | Overwrites `Export Path` in preset.<br>e.g. `C:/Users/jon/my_project/Builds/index.html` |
| `--compile-options` | `string` | - | Arguments to pass to compiler.<br>* `target` is required.<br>* `platform` is set automatically (derived from preset)<br>e.g. `--compile-options target=template_debug --compile-options other-option=other-value`<br>https://docs.godotengine.org/en/4.4/contributing/development/compiling/index.html |
| `--encryption-key` | `string` | - | Key to compile and export with.<br>If not set, build will not be signed.




