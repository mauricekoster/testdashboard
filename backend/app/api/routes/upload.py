from os import stat
from fastapi import APIRouter, HTTPException
from fastapi import UploadFile, Request, BackgroundTasks, status
from typing import List
from tempfile import mkdtemp
from pathlib import Path

import gc

from fastapi.responses import JSONResponse

from app.core.results import process_results

from app.core.utils import (
    get_data,
    save_file,
    check_application_release,
    check_component,
    store_data,
    unpack_content,
)
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()
required_field = ["application", "release", "component"]


def task_process_results(upload_path: str, stored_filename, target_path, application, release, component):
    logger.info(f"TempDir: {upload_path}")
    logger.info(f"Stored filename: {stored_filename}")

    path = Path(upload_path)
    stored_file = path / stored_filename

    if stored_filename.endswith(".tar.gz"):
        unpack_content(target_path, stored_file)
        stored_file.unlink(missing_ok=True)
    else:
        path.mkdir(parents=True, exist_ok=True)
        stored_file.rename(target_path / stored_filename)
    path.rmdir()

    process_results(target_path, application, release, component)

    gc.collect()

    


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def upload_files_new(
    file: UploadFile,
    request: Request,
    background_tasks: BackgroundTasks
):
    data = {}

    temp_path = settings.output_path / "temp"   
    temp_path = mkdtemp(dir=temp_path.absolute().as_posix())

    stored_file = await save_file(temp_path, file)

    async with request.form() as form:
        for k, v in form.items():
            if isinstance(v, str):
                data[k] = v

    # for k, v in request.query_params.items():
    #    data[k] = v

    for field in required_field:
        if field not in data:
            return JSONResponse(
                dict(detail=f"Missing field `{field}`"), status_code=400
            )

    application, release, component = (
        data["application"],
        data["release"],
        data["component"],
    )
    path = check_application_release(application, release)

    meta = get_data(path, "meta.json")
    
    if "locked" in meta:
        # print("has lock state")
        if meta["locked"]:
            # print("locked")
            stored_file.unlink(missing_ok=True)
            Path(temp_path).rmdir()
            # Release is locked. No uploads allowed
            raise HTTPException(status_code=423, detail="Release is locked")

    if "archived" in meta:
        # print("has archived state")
        if meta["archived"]:
            # print("archived")
            stored_file.unlink(missing_ok=True)
            Path(temp_path).rmdir()
            # Release is archived. No uploads allowed
            raise HTTPException(status_code=423, detail="Release is archived")

    path = check_component(path, component, data)

    # Result
    result = {}
    errors: list[str] = []

    # Process meta data
    meta = get_data(path, "meta.json")
    meta.update(data)
    store_data(path, "meta.json", meta)
    result["meta"] = meta

    background_tasks.add_task(task_process_results, temp_path, stored_file.name, path, application, release, component)
    
    return result
