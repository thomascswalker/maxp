from bettermaxtools.utils import files, maxscript

import importlib
importlib.reload(maxscript)

LIGHT_DOME_NAME = "_Dome"
LIGHT_ACCENT_BACK_NAME = "_AccentBack"
LIGHT_ACCENT_SIDE_NAME = "_AccentSide"

def import_light_rig() -> bool:
    print("importing...")
    rigFile = files.relative("..\\resources\\LightRig.max")
    print(rigFile)
    maxscript.rt.mergeMaxFile(rigFile)  # MAXScript

def does_rig_exist() -> bool:
    results = []
    for name in [LIGHT_DOME_NAME, LIGHT_ACCENT_BACK_NAME, LIGHT_ACCENT_SIDE_NAME]:
        node = maxscript.get_node_by_name(name)
        if node is None:
            results.append(False)
            continue
        results.append(True)
    return False if False in results else True
