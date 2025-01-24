from decouple import config

import logging.config

LOG_LEVEL = config("LOG_LEVEL", default="WARNING")

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": LOG_LEVEL,
            "filters": None,
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": LOG_LEVEL,
    },
    "loggers": {
        "main": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)

# GENERAL
# ----------------------------------------------------------------------------------------------------------------------
SOURCE_BRANCH = config("SOURCE_BRANCH", default="main")
TARGET_BRANCH = config("TARGET_BRANCH", default="production")
PTP_MR_NAME = config("PTP_MR_NAME", default="Push To Production")
DOT_GIT_DIR = config("DOT_GIT_DIR", default=".")

# JIRA CONFIG
# ----------------------------------------------------------------------------------------------------------------------
JIRA_PROJECT_URL = config("JIRA_PROJECT_URL", default="")
JIRA_AUTH_LOGIN = config("JIRA_AUTH_LOGIN", default="")
JIRA_AUTH_TOKEN = config("JIRA_AUTH_TOKEN", default="")
JIRA_DONE_STATUS_NAMES = config('JIRA_DONE_STATUS_NAMES', default="Done", cast=lambda v: [s.strip() for s in v.split(',')])


# GITLAB CONFIG
# ----------------------------------------------------------------------------------------------------------------------
GITLAB_URL = config('GITLAB_URL', default='')
GITLAB_PROJECT_ID = config('GITLAB_PROJECT_ID', default='')
GITLAB_PRIVATE_TOKEN = config('GITLAB_PRIVATE_TOKEN', default='')
GITLAB_PTP_LABELS = config('GITLAB_PTP_LABELS', default="", cast=lambda v: [s.strip() for s in v.split(',')])

# MATTERMOST CONFIG
# ----------------------------------------------------------------------------------------------------------------------
MATTERMOST_PTP_MENTION = config("MATTERMOST_PTP_MENTION", default="@channel")
MATTERMOST_CHANNEL = config("MATTERMOST_CHANNEL", default="General")
MATTERMOST_CHANNEL_ID = config("MATTERMOST_CHANNEL_ID", default=0)



