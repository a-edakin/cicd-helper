#!/usr/bin/env python

from src.integrations import (
    RepoManager,
    get_tasks_from_commits,
    generate_description,
    get_new_commits,
    get_todos_from_commits,
)

if __name__ == '__main__':
    commits = get_new_commits()
    tasks = get_tasks_from_commits(commits)
    description = generate_description(tasks)

    repo_manager = RepoManager()
    mr = repo_manager.create_or_update_ptp_mr(description)

    todos = get_todos_from_commits(commits)
    repo_manager.create_todos(mr, todos)
