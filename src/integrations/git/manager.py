from git import Commit, Repo
from src import settings
from src.integrations.structs import ToDo


def get_new_git_commits() -> list[Commit]:
    """Returns a list of all new commits between source and target branches."""
    repo = Repo.init(settings.DOT_GIT_DIR)

    commit_messages = []
    existing_commits = set(c.binsha for c in repo.iter_commits(settings.TARGET_BRANCH))
    for commit in repo.iter_commits(settings.SOURCE_BRANCH):
        if commit.binsha in existing_commits:
            continue
        commit_messages.append(commit)

    return commit_messages


def get_todos_from_git_commits(commits: list[Commit]) -> list[ToDo]:
    """Returns a list of all todos from commit messages."""
    todos = []
    for commit in commits:
        for line in commit.message.split("\n"):
            if "TODO:" not in line and "ToDo:" not in line:
                continue

            try:
                todo_flag_end = line.index("TODO:") + len("TODO:")
            except ValueError:
                todo_flag_end = line.index("ToDo:") + len("ToDo:")

            line = line[todo_flag_end:].strip()

            todos.append(ToDo(commit=commit, text=line))

    return todos


def get_semver_bumps_from_git_commits(commits: list[Commit]) -> tuple[int, int, int]:
    major_bumps = 0
    minor_bumps = 0
    patch_bumps = 0
    for commit in commits:
        if "MAJOR_BUMP" in commit.message:
            major_bumps += 1
        elif "MINOR_BUMP" in commit.message:
            minor_bumps += 1
        else:
            patch_bumps += 1



    return major_bumps, minor_bumps, patch_bumps