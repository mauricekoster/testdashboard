import json
import tarfile
from app.core.config import settings
from pathlib import Path
# Save the uploaded file to the correct sub folder


def make_old_style_folder(appl, component, version, testtype):
    p = settings.output_path / appl / component / version / testtype
    p.mkdir(parents=True, exist_ok=True)
    return p


async def save_file(path: str, file):
    contents = await file.read()

    fn = Path(path) / file.filename
    # print(fn)

    with open(fn, "wb") as f:
        f.write(contents)

    return fn


def get_data(path, filename):
    fn = path / filename

    if fn.exists():
        with open(fn, "r") as f:
            data = json.load(f)
    else:
        data = {}

    return data


def store_data(path, filename, data):
    fn = path / filename

    with open(fn, "w") as f:
        json.dump(data, f, indent=4)


def check_application_release(application, release):
    p = settings.output_path / application / release
    p.mkdir(parents=True, exist_ok=True)

    f = p / "meta.json"
    if not f.exists():
        data = dict(release=release)
        store_data(p, "meta.json", data)

    return p


def check_component(path, component, data):
    p = path / component
    p.mkdir(parents=True, exist_ok=True)

    f = p / "meta.json"
    if not f.exists():
        store_data(p, "meta.json", data)
    else:
        d = get_data(p, "meta.json")
        d.update(data)
        store_data(p, "meta.json", d)
    return p


def unpack_content(path, file):
    with tarfile.open(file, "r:gz") as f:
        f.extractall(path)



