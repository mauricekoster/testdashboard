# source taken from : https://github.com/timdegroot1996/robotframework-dashboard/blob/main/robotframework_dashboard/processors.py

from robot.api import ExecutionResult, ResultVisitor
from robot.result.model import TestCase, TestSuite, Keyword
from datetime import datetime
from pathlib import Path


class OutputProcessor:
    """This class creates an output processor that collects all the relevant data for the database"""

    def get_output_data(self, output_path: Path):
        """This is the main function that is actually called by robotdashboard"""
        output = ExecutionResult(output_path)

        if hasattr(output, "generation_time"):
            generation_time = output.generation_time
        else:
            with open(output_path, "r") as f:
                for line in f:
                    if "<robot" in line:
                        generation_time = line.split('generated="', 1)[1].split('"', 1)[
                            0
                        ]
                        if "T" in generation_time:
                            generation_time = datetime.strptime(
                                generation_time, "%Y-%m-%dT%H:%M:%S.%f"
                            )
                        else:
                            generation_time = datetime.strptime(
                                generation_time, "%Y%m%d %H:%M:%S.%f"
                            )
                        break
        run_list = []
        output.visit(RunProcessor(generation_time, run_list))

        run = run_list[0]

        d = dict(
            runtime=run[0],
            full_name=run[1],
            total=run[3],
            
            fail=run[5],
            skip=run[6],
            elapsed_time=run[7],
            starttime=run[8]
        )
        d['pass'] = run[4]
        return d


class RunProcessor(ResultVisitor):
    """Processer to get the run data"""

    def __init__(self, run_time: datetime, run_list: list):
        self.run_list = run_list
        self.run_time = run_time

    def visit_suite(self, suite: TestSuite):
        stats = suite.statistics

        # handling for older robot versions
        if hasattr(suite, "full_name"):
            full_name = suite.full_name
        else:
            full_name = suite.longname
        if hasattr(suite, "elapsed_time"):
            elapsed_time = round(suite.elapsed_time.total_seconds(), 3)
        else:
            elapsed_time = round(suite.elapsedtime / 1000, 3)
        if hasattr(suite, "start_time"):
            start_time = suite.start_time
        else:
            start_time = suite.starttime

        self.run_list.append(
            (
                self.run_time,
                full_name,
                suite.name,
                stats.total,
                stats.passed,
                stats.failed,
                stats.skipped,
                elapsed_time,
                start_time,
            )
        )
