import importlib
import os
import sys
import threading
from types import ModuleType

import IPython


def import_from_path(name: str, folder: str) -> bool:
    module_path = f"{folder}.{name}"
    importlib.import_module(name=module_path)
    importlib.invalidate_caches()
    print("importing...")
    return module_path in sys.modules


def load_once(dir: str) -> None:
    for item in os.listdir(dir):
        if not os.path.isfile(f"{dir}/{item}") or not item.endswith(".py"):
            continue
        module_name = item[:-3]  # remove ".py"
        module_path = f"{dir}.{module_name}"
        if module_path in sys.modules:
            module = sys.modules[module_path]
            importlib.reload(module)
        else:
            import_from_path(module_name, dir)


def dynamic_loader(dir: str) -> None:
    while True:
        load_once(dir)


def get_module(dir: str, name: str) -> ModuleType:
    return sys.modules[f"{dir}.{name}"]


if __name__ == "__main__":
    directory = sys.argv[1]
    t = threading.Thread(target=dynamic_loader, args=[directory])
    t.daemon = True
    t.start()
    IPython.embed()
