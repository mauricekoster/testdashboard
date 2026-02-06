from pathlib import Path
from fastapi import APIRouter, HTTPException, Request
import json
import shutil
import logging

from app.core.config import settings
from app.core.robotframework import process_robotframework
from app.core.utils import check_application_release, get_data, store_data

from app.api.models import (
    ActiveRelease,
    ApplicationInfo,
    ReleaseInfo,
    Groups,
    GroupInfo,
    GroupMatrix,
    LockState,
)


router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/")
def get_apps():
    """
    Get list of applications avaiable in the store
    """
    p = []
    for folder in settings.output_path.iterdir():
        if folder.is_dir():
            if folder.name in ["lost+found", "temp"]:
                continue

            f = Path(folder) / "meta.json"
            if f.exists():
                with open(f, "r") as file:
                    info = json.load(file)
                d = dict(
                    shortname=info.get("shortname", info.get("name", folder.name)),
                    name=info.get("name", folder.name),
                    icon=info.get("icon", "unknown_document"),
                )
                p.append(d)
            else:
                p.append(folder.name)
    return {"applications": p}


@router.get("/{application}")
def get_application(application) -> ApplicationInfo:
    """
    Get application information
    """
    path = settings.output_path / application
    if not path.exists():
        raise HTTPException(404, "Application not found.")

    f = Path(path) / "meta.json"
    if f.exists():
        info = get_data(path, "meta.json")
        return ApplicationInfo.model_validate(info)

    else:
        raise HTTPException(404, "No application info found.")


@router.patch("/{application}")
def set_application(application, info_in: ApplicationInfo):
    logger.warning(f"{info_in}")
    path = settings.output_path / application
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

    f = Path(path) / "meta.json"
    if f.exists():
        info = get_data(path, "meta.json")
    else:
        info = {}

    if info_in.shortname:
        info["shortname"] = info_in.shortname
    if info_in.name:
        info["name"] = info_in.name
    if info_in.description:
        info["description"] = info_in.description
    if info_in.icon:
        info["icon"] = info_in.icon

    store_data(path, "meta.json", info)

    return info


@router.get("/{application}/active-release")
def get_application_active_release(application) -> ActiveRelease:
    path = settings.output_path / application
    if not path.exists():
        raise HTTPException(404, "Application not found.")

    data = get_data(path, "active_release.json")
    if data:
        return ActiveRelease.model_validate(data)

    raise HTTPException(404, "No active release found.")


@router.patch("/{application}/active-release")
def set_application_active_release(application, info_in: ActiveRelease):
    path = settings.output_path / application
    if not path.exists():
        raise HTTPException(404, "Application not found.")

    f = Path(path) / "active_release.json"
    if f.exists():
        info = get_data(path, "active_release.json")
    else:
        info = {}

    if info_in.active_release:
        info["active_release"] = info_in.active_release

    if info["active_release"]:
        check_application_release(application, info["active_release"])

    store_data(path, "active_release.json", info)

    return info


@router.get("/{application}/groups")
def get_application_groups(application) -> GroupInfo:
    path = settings.output_path / application
    if not path.exists():
        raise HTTPException(404, "Application not found.")

    data = get_data(path, "groups.json")
    if data:
        return GroupInfo.model_validate(data)

    raise HTTPException(404, "No group information found.")


@router.patch("/{application}/groups")
def set_application_groups(application, info_in: GroupInfo) -> GroupInfo:
    print(info_in)
    path = settings.output_path / application
    if not path.exists():
        raise HTTPException(404, "Application not found.")

    groupnames_index = {}
    for i, elem in enumerate(info_in.groupnames):
        groupnames_index[elem] = i

    groupings_index = {}
    for i, elem in enumerate(info_in.groupings):
        name = elem.name
        groupings_index[name] = i

    data = info_in.model_dump()
    data["groupnames_index"] = groupnames_index
    data["groupings_index"] = groupings_index
    store_data(path, "groups.json", data)

    return info_in


@router.get("/{application}/matrix")
def get_application_matrix(application) -> GroupMatrix:
    path = settings.output_path / application
    if not path.exists():
        raise HTTPException(404, "Application not found.")

    data = get_data(path, "matrix.json")
    if data:
        return GroupMatrix.model_validate(data)

    raise HTTPException(404, "No matrix information found.")


@router.patch("/{application}/matrix")
def set_application_matrix(application, info_in: GroupMatrix) -> GroupMatrix:
    path = settings.output_path / application
    if not path.exists():
        raise HTTPException(404, "Application not found.")

    data = info_in.model_dump()
    store_data(path, "matrix.json", data)

    return info_in


@router.get("/{application}/releases")
def get_application_releases(application):
    p = []
    path = settings.output_path / application
    for folder in path.iterdir():
        if folder.is_dir():
            f = Path(folder) / "meta.json"
            if f.exists():
                r = get_data(folder, "meta.json")
                if 'archived' not in r:
                    if 'locked' in r:
                        r['archived'] = r['locked']
                    else:
                        r['archived'] = False
                p.append(r)
    return {"application": application, "releases": p}


def get_component_info(groups, application, release, folder):
    component = folder.name
    d = dict(name=component)

    f = folder / "meta.json"
    if f.exists():
        r = get_data(folder, "meta.json")
        d["info"] = r

    if groups:
        component_index = groups["groupings_index"].get(component, -1)
        if component_index > -1:
            groups = groups["groupings"][component_index]["groups"]
            d["groups"] = groups

    f = folder / "results.json"
    if f.exists():
        r = get_data(folder, "results.json")
        d["results"] = r
    else:
        d["results"] = dict(status="UNKNOWN")

    f = folder / "reports.json"
    if f.exists():
        reports = get_data(folder, "reports.json")
        d["reports"] = reports

    else:
        f = folder / "report.html"
        reports = {}
        if f.exists():
            url = f"/reports/{application}/{release}/{component}/report.html"
            reports["report"] = url

        f = folder / "log.html"
        if f.exists():
            url = f"/reports/{application}/{release}/{component}/log.html"
            reports["log"] = url

        f = folder / "output.xml"
        if f.exists():
            url = f"/reports/{application}/{release}/{component}/output.xml"
            reports["output"] = url
            url = f"/apps/{application}/release/{release}/component/{component}/scan"
            reports["scan"] = url

        d["reports"] = reports

    return d


@router.get("/{application}/release/{release}")
def get_release_info(application, release):
    result = dict(application=application, release=release)
    path = settings.output_path / application / release
    f = Path(path) / "meta.json"
    data = {}
    if f.exists():
        data = get_data(path, "meta.json")

    result.update(data)
    return result

@router.patch("/{application}/release/{release}")
def set_release_info(application, release, info_in: ReleaseInfo):
    path = settings.output_path / application / release
    f = Path(path) / "meta.json"
    data = {}
    if f.exists():
        data = get_data(path, "meta.json")

    update_data = info_in.model_dump(exclude_unset=True)
    # if 'release' in update_data:
    #     del update_data['release']
        
    print(f"app: {application} release: {release} info: {update_data}")
    data.update(update_data)

    store_data(path, "meta.json", data)

    return data

@router.get("/{application}/release/{release}/lock")
def get_release_lock(application, release):
    path = settings.output_path / application / release
    f = Path(path) / "meta.json"
    data = {}
    if f.exists():
        data = get_data(path, "meta.json")
        if "locked" in data:
            return LockState(locked=data["locked"])
        else:
            return LockState(locked=False)

    return LockState(locked=False)


@router.patch("/{application}/release/{release}/lock")
def set_release_lock(application, release, lockstate: LockState):
    path = settings.output_path / application / release
    f = Path(path) / "meta.json"
    data = {}
    if f.exists():
        data = get_data(path, "meta.json")

    print(f"app: {application} release: {release} locked: {lockstate.locked}")
    data["locked"] = lockstate.locked

    store_data(path, "meta.json", data)

    return data


@router.delete("/{application}/release/{release}")
def delete_application_release(application: str, release: str):
    path = settings.output_path / application / release
    if path.exists():
        shutil.rmtree(path, ignore_errors=True)
        return dict(message=f"Release {release} for application {application} deleted.")

    raise HTTPException("Something went wrong")


@router.get("/{application}/release/{release}/components")
def get_application_release_components(application, release):
    components = []
    data = dict(application=application, release=release)
    path = settings.output_path / application
    groups = get_data(path, "groups.json")

    path = settings.output_path / application / release
    f = Path(path) / "meta.json"
    if f.exists():
        for folder in path.iterdir():
            if folder.is_dir():
                d = get_component_info(groups, application, release, folder)
                components.append(d)

        data["components"] = components

    return data


@router.get("/{application}/release/{release}/component/{component}")
def get_component(application: str, release: str, component: str):
    path = settings.output_path / application
    groups = get_data(path, "groups.json")
    path = settings.output_path / application / release / component
    if path.exists():
        f = path / "meta.json"
        if f.exists():
            data = get_component_info(groups, application, release, path)
            return data

    raise HTTPException(404, "Component not found.")


@router.post("/{application}/release/{release}/component/{component}/scan")
def scan_component_directory(application, release, component):
    print(f"Scanning: {application} {release} {component}")

    result = {}
    path = settings.output_path / application / release / component
    if path.exists():
        f = path / "meta.json"
        if f.exists():
            f = path / "output.xml"
            if f.exists():
                rf, _ = process_robotframework(path)
                result.update(rf)

    return result


def get_component_results(application, release, folder):
    component = folder.name
    d = dict(name=component)

    f = folder / "results.json"
    if f.exists():
        r = get_data(folder, "results.json")
        d["pass"] = r["total"]["pass"]
        d["fail"] = r["total"]["fail"]
        d["skip"] = r["total"]["skip"]
        for k in ['status', 'starttime', 'endtime', 'elapsedtime']:
            if k in r:
                d[k] = r[k]
    else:
        d["status"] = "UNKNOWN"

    return d


@router.get("/{application}/release/{release}/results")
def get_application_release_results(application, release):
    result = dict(application=application, release=release)
    path = settings.output_path / application / release
    f = Path(path) / "meta.json"
    components = {}

    if f.exists():
        for folder in path.iterdir():
            if folder.is_dir():
                d = get_component_results(application, release, folder)
                components[d["name"]] = d

        result["components"] = components
    return result
