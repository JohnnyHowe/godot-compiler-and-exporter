Wraps the build process.
1. Compiles new build template (if required) (uses https://github.com/JohnnyHowe/godot-template-creator)
2. exports The project

# Running
```
python export_project.py <project-root> <godot-version> <export-preset> <output-path>
```

# Parameters
| Name | Required | Type | Default | Note |
| - | - | - | - | - |
| `project-root` | ✅ | `Path` | - | Path to the project to export. |
| `godot-version` | ✅ | `string` | - | What version to use. e.g `4.6`.<br>See https://github.com/godotengine/godot/branches for options.
| `export-preset` | ✅ | `string` | - | The name of the export preset set in the project. |
| `output_path` | ✅ | `Path` | - | Where to export the project to.<br>e.g. `C:/Users/jon/my_project/Builds/index.html` |
| `--compile_options` | ❌ | `list` | empty | Additional options to compile the template with. (`platform` and `target` are always set).<br>e.g. `javascript_eval=no,threads=no`<br>See https://docs.godotengine.org/en/4.4/contributing/development/compiling/index.html for options.
| `--debug` | ❌ | `bool` | `false` | Debug or release export
| `--encryption-key` | ❌ | `string` | - | Key to compile and export with.<br>If not set, build will not be signed.

options to add
* force recompile 