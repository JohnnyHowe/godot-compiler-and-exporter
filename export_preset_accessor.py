import argument_accessor
from standalone.export_preset_access import ExportPresetAccessor


preset_accessor = ExportPresetAccessor(argument_accessor.project_root / "export_presets.cfg")