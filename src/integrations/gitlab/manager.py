import logging
from functools import cached_property
from typing import cast

import gitlab
from gitlab.v4.objects import Project, ProjectMergeRequest

from src import settings
from src.integrations.structs import BaseTask, ToDo

logger = logging.getLogger(__name__)


def generate_gitlab_description(tasks: list[BaseTask]):
    description = ""
    for task in sorted(tasks):
        done = "x" if task.done else " "
        description += f"- [{done}] {task.id} - {task.name}\n"
    return description


class GitlabManager:
    def __init__(self):
        self.api = gitlab.Gitlab(url=settings.GITLAB_URL, private_token=settings.GITLAB_PRIVATE_TOKEN)

    @cached_property
    def project(self) -> Project:
        return self.api.projects.get(settings.GITLAB_PROJECT_ID)

    def create_ptp_mr(self, description: str) -> ProjectMergeRequest:
        logger.info("Creating new PTP merge request")
        mr = cast(ProjectMergeRequest, self.project.mergerequests.create({
            'source_branch': settings.SOURCE_BRANCH,
            'target_branch': settings.TARGET_BRANCH,
            'title': settings.PTP_MR_NAME,
            "description": description,
            'labels': settings.GITLAB_PTP_LABELS,
        }))
        logger.info("Created PTP merge request with id=%s", mr.id)
        return mr

    def get_ptp_mr(self) -> ProjectMergeRequest | None:
        mrs = self.project.mergerequests.list(
            state="opened",
            source_branch=settings.SOURCE_BRANCH,
            target_branch=settings.TARGET_BRANCH,
        )
        for mr in mrs:
            if mr.title != settings.PTP_MR_NAME:
                pass
            logger.info("PTP merge request with id=%s found.", mr.id)
            return cast(ProjectMergeRequest, mr)

        logger.info(
            "PTP merge request with source_branch=%s and target_branch=%s and title=%s, not found",
            settings.SOURCE_BRANCH,
            settings.TARGET_BRANCH,
            settings.PTP_MR_NAME,
        )
        return None

    def create_or_update_ptp_mr(self, description: str) -> ProjectMergeRequest:
        logger.info("Creating/updating PTP merge request.")
        mr = self.get_ptp_mr()
        if mr is not None:
            logger.info("Updating PTP merge request with id=%s", mr.id)
            mr.description = description
            mr.save()
            return mr

        return self.create_ptp_mr(description)

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
