import gc
import importlib
import inspect
import os
import sys
import threading
import time
from types import ModuleType
from typing import Any, Callable

import IPython


def import_from_path(name: str, folder: str) -> bool:
    module_path = f"{folder}.{name}"
    importlib.import_module(name=module_path)
    importlib.invalidate_caches()
    print("importing...")
    return module_path in sys.modules


def get_classes(module: ModuleType) -> dict[str, type]:
    return {
        name: obj for (name, obj) in inspect.getmembers(module) if inspect.isclass(obj)
    }


def get_functions(module: ModuleType) -> dict[str, Callable]:
    return dict(
        inspect.getmembers(
            module, lambda m: inspect.isfunction(m) or inspect.ismethod(m)
        )
    )


def get_class_objects(cls: type) -> list[Any]:
    return [obj for obj in gc.get_referrers(cls) if isinstance(obj, cls)]


def match_new(name: str, module: ModuleType) -> type | Callable:
    """Match functions/classes by their name.
    NOTE that this will only work if the class name was not changed.
    NOTE that this does not support overloading."""

    return next(obj for obj_name, obj in inspect.getmembers(module) if name == obj_name)


def reload_module(module: ModuleType) -> None:
    functions: dict[str, Callable] = get_functions(module)
    classes = get_classes(module)
    module = importlib.reload(module)

    for (
        name,
        func,
    ) in functions.items():  # y this not work :(
        func.__code__ = match_new(name, module).__code__
    for cls_name, cls in classes.items():
        for obj in get_class_objects(cls):
            obj.__class__ = match_new(cls_name, module)


def get_module(dir: str, name: str) -> ModuleType:
    return sys.modules[f"{dir}.{name}"]


def load_once(dir: str) -> None:
    for item in os.listdir(dir):
        if not os.path.isfile(f"{dir}/{item}") or not item.endswith(".py"):
            continue
        module_name = item[:-3]  # remove ".py"
        module_path = f"{dir}.{module_name}"
        if module_path in sys.modules:
            module = sys.modules[module_path]
            reload_module(module)
            # importlib.reload(module)
        else:
            import_from_path(module_name, dir)


def dynamic_loader(dir: str) -> None:
    while True:
        load_once(dir)
        time.sleep(1)


if __name__ == "__main__":
    directory = sys.argv[1]
    t = threading.Thread(target=dynamic_loader, args=[directory])
    t.daemon = True
    t.start()
    IPython.embed()
