from pathlib import Path


def process_surefire(path: Path, subfolder, application, release, component):
    if subfolder:
        url = f"/reports/{application}/{release}/{component}/{subfolder}"
    else:
        url = f"/reports/{application}/{release}/{component}"

    return {}, {f"{subfolder}": f"{url}/surefire.html"}, []
