from .battery import battery_case
from .water import water_case
from .robot import robot_case
from .railway import railway_case

_FACTORIES = {
    "battery": battery_case,
    "water": water_case,
    "robot": robot_case,
    "railway": railway_case,
}


def list_cases():
    return sorted(_FACTORIES)


def get_case(name, **kwargs):
    try:
        return _FACTORIES[name](**kwargs)
    except KeyError as exc:
        raise KeyError(f"unknown domain {name!r}; choose from {list_cases()}") from exc
