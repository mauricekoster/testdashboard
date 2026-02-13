from nicegui import ui, APIRouter

from .templates.project import projectpage
from app.core.project import Project
from app.components.project import (
    ProjectDashboard, 
    ProjectDefine, 
    ProjectDesign, 
    ProjectPlan, 
    ProjectRun,
    ProjectTrack,
    ProjectResolve,
    ProjectAnalyze
)

router = APIRouter()


@router.page("/project/{projectId}")
def show_project_dashboard(projectId):
    project = Project(projectId)
    with projectpage(project, "dashboard"):
        ProjectDashboard(project)


@router.page("/project/{projectId}/define")
def show_project_define(projectId):
    project = Project(projectId)
    with projectpage(project, "define"):
        ProjectDefine(project)


@router.page("/project/{projectId}/design")
def show_project_design(projectId):
    project = Project(projectId)
    with projectpage(project, "design"):
        ProjectDesign(project)


@router.page("/project/{projectId}/plan")
def show_project_plan(projectId):
    project = Project(projectId)
    with projectpage(project, "plan"):
        ProjectPlan(project)


@router.page("/project/{projectId}/run")
def show_project_run(projectId):
    project = Project(projectId)
    with projectpage(project, "run"):
        ProjectRun(project)


@router.page("/project/{projectId}/track")
def show_project_track(projectId):
    project = Project(projectId)
    with projectpage(project, "track"):
        ProjectTrack(project)


@router.page("/project/{projectId}/resolve")
def show_project_resolve(projectId):
    project = Project(projectId)
    with projectpage(project, "resolve"):
        ProjectResolve(project)


@router.page("/project/{projectId}/analyze")
def show_project_dashboard(projectId):
    project = Project(projectId)
    with projectpage(project, "ranalyzen"):
        ProjectAnalyze(project)
