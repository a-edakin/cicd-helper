import logging
from functools import cached_property
from typing import cast

import gitlab
from gitlab.v4.objects import Project, ProjectMergeRequest
from semver import Version

from src import settings
from src.integrations.structs import BaseTask, ToDo

logger = logging.getLogger(__name__)


def generate_gitlab_description(tasks: list[BaseTask]):
    description = ""
    for task in sorted(tasks):
        done = "x" if task.done else " "
        description += f"- [{done}] {task.id} - {task.name}\n"
    return description


def generate_gitlab_title(previous_version: Version | None = None, next_version: Version | None = None):
    if next_version is not None:
        previous_version = previous_version or Version(major=0)
        return f"{settings.PTP_MR_NAME} [{previous_version}] -> [{next_version}]"

    return settings.PTP_MR_NAME


class GitlabManager:
    def __init__(self):
        self.api = gitlab.Gitlab(url=settings.GITLAB_URL, private_token=settings.GITLAB_PRIVATE_TOKEN)

    @cached_property
    def project(self) -> Project:
        return self.api.projects.get(settings.GITLAB_PROJECT_ID)

    def get_previous_semver(self) -> Version | None:
        # TODO: Temporary fix for issue when on CICD only remote branches are present
        source_branch = settings.SOURCE_BRANCH.replace("remotes/origin/", "")
        target_branch = settings.TARGET_BRANCH.replace("remotes/origin/", "")
        mrs = self.project.mergerequests.list(
            state="merged",
            source_branch=source_branch,
            target_branch=target_branch,
            get_all=False,
        )

        previous_mr = None
        for mr in mrs:
            if mr.title.startswith(settings.PTP_MR_NAME):
                previous_mr = mr
                logger.info("Previous PTP with id=%s found.", mr.id)
                break

        if previous_mr is None:
            return None

        versions = mr.title.replace(f"{settings.PTP_MR_NAME} ", "").split(" -> ")
        if len(versions) != 2:
            return None

        previous_version_raw = versions[0].replace("[", "").replace("]", "")

        try:
            return Version.parse(previous_version_raw)
        except ValueError as err:
            logger.error("Couldn't parse previous version: %s", previous_version_raw, exc_info=err)
            return None


    def create_ptp_mr(self, title: str, description: str) -> ProjectMergeRequest:
        logger.info("Creating new PTP merge request")
        # TODO: Temporary fix for issue when on CICD only remote branches are present
        source_branch = settings.SOURCE_BRANCH.replace("remotes/origin/", "")
        target_branch = settings.TARGET_BRANCH.replace("remotes/origin/", "")
        mr = cast(ProjectMergeRequest, self.project.mergerequests.create({
            'source_branch': source_branch,
            'target_branch': target_branch,
            'title': title,
            "description": description,
            'labels': settings.GITLAB_PTP_LABELS,
        }))
        logger.info("Created PTP merge request with id=%s", mr.id)
        return mr

    def get_ptp_mr(self) -> ProjectMergeRequest | None:
        # TODO: Temporary fix for issue when on CICD only remote branches are present
        source_branch = settings.SOURCE_BRANCH.replace("remotes/origin/", "")
        target_branch = settings.TARGET_BRANCH.replace("remotes/origin/", "")
        mrs = self.project.mergerequests.list(
            state="opened",
            source_branch=source_branch,
            target_branch=target_branch,
            get_all=False,
        )
        for mr in mrs:
            if not mr.title.startswith(settings.PTP_MR_NAME):
                continue
            logger.info("PTP merge request with id=%s found.", mr.id)
            return cast(ProjectMergeRequest, mr)

        logger.info(
            "PTP merge request with source_branch=%s and target_branch=%s and title=%s, not found",
            source_branch,
            target_branch,
            settings.PTP_MR_NAME,
        )
        return None

    def create_or_update_ptp_mr(self, title: str, description: str) -> ProjectMergeRequest:
        logger.info("Creating/updating PTP merge request.")
        mr = self.get_ptp_mr()
        if mr is not None:
            logger.info("Updating PTP merge request with id=%s", mr.id)
            mr.title = title
            mr.description = description
            mr.save()
            return mr

        return self.create_ptp_mr(title, description)

    def create_todos(self, mr: ProjectMergeRequest, todos: list[ToDo]) -> None:
        discussions = mr.discussions.list(get_all=True)
        existing_todos = [d.attributes["notes"][0]["body"] for d in discussions]
        for todo in todos:
            todo_text = f"Commit: {todo.commit.hexsha} TODO: {todo.text}"

            if todo_text in existing_todos:
                logger.info("TODO `%s` is not created because it already exist.", todo.short)
                continue

            mr.discussions.create({'body': todo_text})
            logger.info("TODO `%s` is created.", todo.short)
