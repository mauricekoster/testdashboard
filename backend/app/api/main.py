from fastapi import APIRouter

from app.api.routes import apps, health, login, private, upload, utils
from app.api.routes.define import (
    requirements,
    requirement_types,
    requirement_tags,
    risks,
    risk_classifications,
    risk_tags
)
from app.api.routes.design import (
    folders,
    test_cases,
    test_case_tags
)
from app.api.routes.plan import (
    milestones,
    milestone_types,
    test_runs,
    test_run_tags,
    my_test_runs
)
from app.api.routes.track import (
    test_results,
    test_result_statuses
)
from app.api.routes.resolve import (
    issues,
    issue_categories,
    issue_priorities,
    issue_resolutions,
    issue_statuses,
    issue_tasks,
    issue_tags,
    my_issues,
    my_issue_tasks
)
from app.api.routes.general import (
    applications, 
    custom_fields, 
    environments, 
    projects, 
    symbols, 
    teams,
    test_types,
    users,
    versions,
    webhooks
    )

api_router = APIRouter()

# Login
api_router.include_router(login.router, tags=["login"])

# Admin/maintenance stuff
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(private.router, prefix="/private", tags=["private"])
api_router.include_router(health.router, prefix="/health", tags=["health"])

# Test Report Server; needs rework
api_router.include_router(apps.router, prefix="/apps", tags=["apps"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])

# Define
api_router.include_router(requirements.router, prefix="/requirements", tags=["Requirements"])
api_router.include_router(requirement_types.router, prefix="/requirement-types", tags=["Requirement Types"])
api_router.include_router(requirement_tags.router, prefix="/requirement-tags", tags=["Requirement Tags"])
api_router.include_router(risks.router, prefix="/risks", tags=["Risks"])
api_router.include_router(risk_classifications.router, prefix="/risk-classifications", tags=["Risk Classifications"])
api_router.include_router(risk_tags.router, prefix="/risk-tags", tags=["Risk Tags"])

# Design
api_router.include_router(folders.router, prefix="/folders", tags=["Folders"])
api_router.include_router(test_cases.router, prefix="/test-cases", tags=["Test Cases"])
api_router.include_router(test_case_tags.router, prefix="/test-case-tags", tags=["Test Case Tags"])

# Plan
api_router.include_router(milestones.router, prefix="/milestones", tags=["Milestones"])
api_router.include_router(milestone_types.router, prefix="/milestone-types", tags=["Milestone Types"])
api_router.include_router(test_runs.router, prefix="/test-runs", tags=["Test Runs"])
api_router.include_router(test_run_tags.router, prefix="/test-run-tags", tags=["Test Run Tags"])
api_router.include_router(my_test_runs.router, prefix="/my-test-runs", tags=["My Test Runs"])

# Track
api_router.include_router(test_results.router, prefix="/test-results", tags=["Test Results"])
api_router.include_router(test_result_statuses.router, prefix="/test-result-statuses", tags=["Test Result Statuses"])

# Issues
api_router.include_router(issues.router, prefix="/issues", tags=["Issues"])
api_router.include_router(issue_categories.router, prefix="/issue-categories", tags=["Issue Categories"])
api_router.include_router(issue_priorities.router, prefix="/issue-priorities", tags=["Issue Priorities"])
api_router.include_router(issue_resolutions.router, prefix="/issue-resolutions", tags=["Issue Resolutions"])
api_router.include_router(issue_statuses.router, prefix="/issue-statuses", tags=["Issue Statuses"])
api_router.include_router(issue_tasks.router, prefix="/issue-tasks", tags=["Issue Tasks"])
api_router.include_router(issue_tags.router, prefix="/issue-tags", tags=["Issue Tags"])
api_router.include_router(my_issues.router, prefix="/my-issues", tags=["My Issues"])
api_router.include_router(my_issue_tasks.router, prefix="/my-issue-tasks", tags=["My Issue Tasks"])

# General
api_router.include_router(applications.router, prefix="/applications", tags=["Applications"])
api_router.include_router(custom_fields.router, prefix="/custom-fields", tags=["Custom Fields"])
api_router.include_router(environments.router, prefix="/environments", tags=["Environments"])
api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])
api_router.include_router(symbols.router, prefix="/symbols", tags=["Symbols"])
api_router.include_router(teams.router, prefix="/teams", tags=["Teams"])
api_router.include_router(test_types.router, prefix="/test-types", tags=["Test Types"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(versions.router, prefix="/versions", tags=["Versions"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])
