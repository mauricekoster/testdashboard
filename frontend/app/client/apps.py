from . import APIException
from .main import openapi
from operator import itemgetter

from app.models import ApplicationInfo


def get_apps():
    response = openapi.get("/apps/")
    if response.status_code == 200:
        result = response.json()
        apps = result["applications"]
        return apps

    else:
        raise APIException(f"get_apps: {response.json()}")


def get_groups(app: str):
    response = openapi.get(f"/apps/{app}/groups")
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        raise APIException(f"get_groups: {response.json()}")


def set_groups(app: str, data: dict):
    
    response = openapi.patch(f"/apps/{app}/groups", data)
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        raise APIException(f"set_groups: {response.json()}")


def get_matrix(app: str):
    response = openapi.get(f"/apps/{app}/matrix")
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        raise APIException(f"get_matrix: {response.json()}")


def set_matrix(app: str, data: dict):
    
    response = openapi.patch(f"/apps/{app}/matrix", data)
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        raise APIException(f"set_matrix: {response.json()}")


def get_application(app: str):
    response = openapi.get(f"/apps/{app}")
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        raise APIException(f"get_application: {response.json()}")


def set_application(app: str, data: ApplicationInfo) -> ApplicationInfo:
    
    response = openapi.patch(f"/apps/{app}", data.model_dump_json())
    if response.status_code == 200:
        return ApplicationInfo.model_validate_json(response.content)
    else:
        raise APIException(f"set_application: {response.json()}")


def get_active_release(app: str):
    response = openapi.get(f"/apps/{app}/active-release")
    if response.status_code == 200:
        result = response.json()
        return result["active_release"]
    else:
        raise APIException(f"get_active_release: {response.json()}")


def set_active_release(app: str, release: str):
    data = dict(active_release=release)
    response = openapi.patch(f"/apps/{app}/active-release", data)
    if response.status_code == 200:
        result = response.json()
        return result["active_release"]
    else:
        raise APIException(f"set_active_release: {response.json()}")


def get_releases(app: str):
    response = openapi.get(f"/apps/{app}/releases")
    if response.status_code == 200:
        result = response.json()
        releases = result["releases"]
        releases = sorted(releases, key=lambda x: x['release'])
        return releases
    else:
        raise APIException(f"get_releases: {response.json()}")


def get_release_info(app: str, release: str):
    response = openapi.get(f"/apps/{app}/release/{release}")
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        raise APIException(f"get_release_info: {response.json()}")


def update_release_info(app: str, release: str, data: dict):
    response = openapi.patch(f"/apps/{app}/release/{release}", data)
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        raise APIException(f"update_release_info: {response.json()}")


def get_release_lock(app: str, release: str):
    response = openapi.get(f"/apps/{app}/release/{release}/lock")
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        raise APIException(f"get_release_lock: {response.json()}")


def set_release_lock(app: str, release: str, lock: bool) -> bool:
    data = dict(locked=lock)
    response = openapi.patch(f"/apps/{app}/release/{release}/lock", data)
    if response.status_code == 200:
        result = response.json()
        return bool(result["locked"])
    else:
        raise APIException(f"set_release_lock: {response.json()}")



def delete_release(app: str, release: str):
    response = openapi.delete(f"/apps/{app}/release/{release}")
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        raise APIException(f"delete_release: {response.json()}")


def get_release_components(app: str, release: str):
    response = openapi.get(f"/apps/{app}/release/{release}/components")
    if response.status_code == 200:
        result = response.json()
        components = result["components"]
        newlist = sorted(components, key=itemgetter("name"))
        return newlist
    else:
        raise APIException(f"get_release_components: {response.json()}")


def get_release_results(app: str, release: str):
    response = openapi.get(f"/apps/{app}/release/{release}/results")
    if response.status_code == 200:
        result = response.json()
        components = result["components"]
        
        return components
    else:
        raise APIException(f"get_release_results: {response.json()}")
