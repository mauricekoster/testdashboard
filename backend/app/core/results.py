from pathlib import Path
from .robotframework import process_robotframework
from .xunit import process_xunit
from .surefire import process_surefire
from .htmlreport import process_htmlreport

from app.core.utils import store_data
import logging

logger = logging.getLogger(__name__)


def process_folder_results(path: Path, subfolder, application, release, component):
    errors = []
    results = {}
    reports = None

    if subfolder:
        p = path / subfolder
    else:
        p = path

    #
    # Process RobotFramework files if applicable
    output_xml = p / "output.xml"
    if output_xml.exists():
        results, reports, errors = process_robotframework(
            p, application, release, component
        )
        return results, reports, errors

    if len(list(p.glob("*.xml"))) > 0:
        results, reports, errors = process_xunit(
            path, subfolder, application, release, component
        )
        return results, reports, errors

    fn = p / "surefire.html"
    if fn.exists():
        results, reports, errors = process_surefire(
            path, subfolder, application, release, component
        )
        return results, reports, errors

    fn = p / "index.html"
    if fn.exists():
        results, reports, errors = process_htmlreport(
            path, subfolder, application, release, component
        )
        return results, reports, errors

    return results, reports, errors


def process_results(path: Path, application, release, component):
    errors = []
    results = {}
    reports = {}

    logger.info(f"Start processing. application={application} release={release} component={component}")

    results, reports, errors = process_folder_results(
        path, None, application, release, component
    )

    logger.debug(f"results {results} | reports {reports}")

    if not results and not reports and not errors:
        # Try subfolder
        logger.debug("SUBFOLDERS")
        reports = {}

        for p in path.glob("*"):
            if p.is_dir():
                results_sub, reports_sub, errors_sub = process_folder_results(
                    path, p.name, application, release, component
                )
                logger.debug(f": results {results_sub} | reports {reports_sub}")

                if results_sub:
                    if "total" in results_sub:
                        if "total" in results:
                            for x in ["pass", "fail", "skip"]:
                                results["total"][x] += results_sub["total"][x]
                        else:
                            results["total"] = results_sub["total"]

                    if "tags" in results_sub:
                        if "tags" in results:
                            results["tags"].extend(results_sub["tags"])
                        else:
                            results["tags"] = results_sub["tags"]

                    if "status" in results_sub:
                        if "status" in results:
                            if results["status"] == "UNKNOWN":
                                results["status"] = results_sub["status"]
                            elif results["status"] == "PASS":
                                if results_sub["status"] == "FAIL":
                                    results["status"] = "FAIL"

                        else:
                            results["status"] = results_sub["status"]
                if reports_sub:
                    if isinstance(reports_sub, list):
                        reports[str(p.name)] = list(reports_sub)
                    else:
                        reports.update(reports_sub)

    if results:
        store_data(path, "results.json", results)
    if reports:
        store_data(path, "reports.json", reports)

    logger.info(f"Processing results done. application={application} release={release} component={component}")
