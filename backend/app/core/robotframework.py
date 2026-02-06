import shutil
import xml.etree.ElementTree as ET
import logging
from pathlib import Path

from .robotframework_processors import OutputProcessor
from robot.api import ExecutionResult

logger = logging.getLogger(__name__)
import datetime

from pprint import pprint

def process_output_xml(path):
    output_xml = path / "output.xml"

    execution_results = ExecutionResult(output_xml)
    statistics = execution_results.statistics.to_dict()
    
    output_processor = OutputProcessor()
    output_data = output_processor.get_output_data(output_xml)

    # pprint(statistics)
    # pprint(output_data)

    d = {}
    d["status"] = "PASS"
    errors = []

    # print(output_data)
    if 'starttime' in output_data:
        if output_data['starttime'] is not None:
            d['starttime'] = output_data['starttime'].isoformat()
            new_datetime = output_data['starttime'] + datetime.timedelta(seconds=output_data['elapsed_time'])
            d['endtime'] = new_datetime.isoformat()
    
    if 'elapsed_time' in output_data:
        d['elapsedtime'] = output_data['elapsed_time']

    d["total"] = statistics['total']
    if d["total"]["fail"] > 0:
        d["status"] = "FAIL"
    
    tag_results = []
    for tag in statistics['tags']:
        results = {}
        tag_name = tag['label']
        for x in ["pass", "fail", "skip"]:
            if x in tag:
                results[x] = int(tag.get(x, 0))
        tag_results.append(dict(name=tag_name, results=results))
    if tag_results:
        d["tags"] = tag_results

    output_xml.unlink()

    # pprint(d)

    return d, errors


def process_html(path: Path, application, release, component):
    reports = {}

    url = f"/reports/{application}/{release}/{component}"

    f = path / "report.html"
    if f.exists():
        reports["report"] = f"{url}/report.html"

    f = path / "log.html"
    if f.exists():
        reports["log"] = f"{url}/log.html"

    return reports


def cleanup_directories(path):
    p = path / "browser" / "traces"

    if p.exists():
        shutil.rmtree(p)


def process_robotframework(path, application, release, component):
    logger.info("Processing RobotFramework results")
    result = {}
    errors = []

    d, process_errors = process_output_xml(path)
    result.update(d)
    errors.extend(process_errors)

    reports = process_html(path, application, release, component)
    cleanup_directories(path)

    return result, reports, errors
