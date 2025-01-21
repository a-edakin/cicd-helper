import logging
import re

from git import Commit
from jira import JIRA, JIRAError

from src import settings
from src.integrations.jira.structs import JiraTask

logger = logging.getLogger(__name__)


def get_jira_tasks_from_commits(commits: list[Commit]) -> list[JiraTask]:
    task_ids = set()
    for commit in commits:
        task_id = re.search(r"[A-Z]+-[0-9]+", commit.summary)
        if task_id is None:
            continue
        task_ids.add(task_id.group())

    auth_jira = JIRA(settings.JIRA_PROJECT_URL, basic_auth=(settings.JIRA_AUTH_LOGIN, settings.JIRA_AUTH_TOKEN))

    tasks = []
    for task_id in list(task_ids):
        logger.info("Requesting Jira task %s", task_id)
        try:
            issue = auth_jira.issue(task_id, fields='summary,status')
        except JIRAError as err:
            logger.error("Failed to retrieve Jira task %s: %s", task_id, err.args[0])
            continue

        tasks.append(JiraTask(
            id=task_id,
            name=issue.fields.summary,
            done=issue.fields.status.name in settings.JIRA_DONE_STATUS_NAMES,
        ))

    return tasks
