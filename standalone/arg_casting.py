from types import NoneType
from typing import Type, Union, get_args, get_origin


def cast(value, target_type: Type):
	for parser in [
		_union_caster,
		_dict_caster,
		_generic_caster,
	]:
		try:
			return parser(value, target_type)
		except:
			pass
	raise TypeError(f"Could not cast {value} to {target_type}")


def _generic_caster(value, target_type: Type):
	return target_type(value)


def _dict_caster(value, target_type: Type) -> dict:
	if not target_type == dict:
		raise TypeError()

	data = {}
	if value is None:
		return data
	for part in value.split(","):
		key, value = part.split("=")
		data[key.strip()] = value.strip()
	return data


def _union_caster(value, target_type: Type):
	if not get_origin(target_type) is Union:
		raise TypeError()

	for potential_type in get_args(target_type):
		try:
			return cast(value, potential_type)
		except:
			pass