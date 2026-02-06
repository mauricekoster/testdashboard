from pathlib import Path
import logging
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)


def process_xunix_file(xml_file: Path):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        if root.tag in ["testsuites", "testsuite"]:
            result = {}
            result["status"] = "UNKNOWN"
            if "tests" in root.attrib:
                tests = int(root.get("tests", 0))

                if tests > 0:
                    failures = int(root.get("failures", 0))
                    errors = int(root.get("errors", 0))
                    skip = int(root.get("skipped", 0))

                    fails = failures + errors
                    _pass = tests - fails - skip

                    result["pass"] = _pass
                    result["fail"] = fails
                    result["skip"] = skip

                    result = (_pass, fails, skip)

                else:
                    result = None

            return True, result

    except ET.ParseError:
        return False, None

    return False, None


def process_xunit(path: Path, subfolder, application, release, component):
    logger.info("Processing XML files")
    results = {}
    total_pass, total_fail, total_skip = 0, 0, 0
    tags = []
    reports = []

    if subfolder:
        p = path / subfolder
        url = f"/reports/{application}/{release}/{component}/{subfolder}"
    else:
        p = path
        url = f"/reports/{application}/{release}/{component}"

    for fn in p.glob("*.xml"):
        ok, result = process_xunix_file(fn)
        if ok and result is not None:
            # print(f"file: {fn} result: {result}")
            ps, f, s = result
            total_pass += ps
            total_fail += f
            total_skip += s

            d = {}
            d["name"] = fn.name
            d["results"] = dict(fail=f, skip=s)
            d["results"]["pass"] = ps

            tags.append(d)
            report = dict(name=fn.stem, url=f"{url}/{fn.name}")
            reports.append(report)

    results["total"] = dict(fail=total_fail, skip=total_skip)
    results["total"]["pass"] = total_pass

    if total_pass == 0 and total_fail == 0 and total_skip == 0:
        return {}, {}, []

    if total_fail > 0:
        results["status"] = "FAIL"
    elif total_pass > 0:
        results["status"] = "PASS"
    else:
        results["status"] = "UNKNOWN"

    if tags:
        results["tags"] = tags

    return results, reports, []
