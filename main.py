#!/usr/bin/env python

from src.integrations import (
    RepoManager,
    generate_title, get_semver_bumps_from_commits, get_tasks_from_commits,
    generate_description,
    get_new_commits,
    get_todos_from_commits,
)
from src import settings
from src.versions import calculate_next_semver

if __name__ == '__main__':
    commits = get_new_commits()
    tasks = get_tasks_from_commits(commits)
    description = generate_description(tasks)

    repo_manager = RepoManager()

    if settings.TRACK_SEMVER:
        previous_version = repo_manager.get_previous_semver()
        version_bumps = get_semver_bumps_from_commits(commits)
        next_version = calculate_next_semver(previous_version, version_bumps)
        title = generate_title(previous_version, next_version)
    else:
        title = generate_title()

    mr = repo_manager.create_or_update_ptp_mr(title, description)

    todos = get_todos_from_commits(commits)
    repo_manager.create_todos(mr, todos)
