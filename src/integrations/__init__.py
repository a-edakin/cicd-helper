from src.integrations.git.manager import get_new_git_commits, get_todos_from_git_commits
from src.integrations.gitlab.manager import GitlabManager, generate_gitlab_description
from src.integrations.jira.manager import get_jira_tasks_from_commits

RepoManager = GitlabManager
get_new_commits = get_new_git_commits
get_todos_from_commits = get_todos_from_git_commits
get_tasks_from_commits = get_jira_tasks_from_commits
generate_description = generate_gitlab_description

__all__ = (
    "RepoManager",
    "get_new_commits",
    "get_todos_from_commits",
    "get_tasks_from_commits",
    "generate_description",
)
