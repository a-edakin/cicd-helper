import logging

from semver import Version

logger = logging.getLogger(__name__)


def calculate_next_semver(previous_version: Version | None, version_bumps: tuple[int, int, int]) -> Version:
    previous_version = previous_version or Version(major=0)

    new_version = Version(major=previous_version.major, minor=previous_version.minor, patch=previous_version.patch)

    if version_bumps[0] > 0:
        new_version = new_version.bump_major()
    elif version_bumps[1] > 0:
        new_version = new_version.bump_minor()
    elif version_bumps[2] > 0:
        new_version = new_version.bump_patch()

    logging.info("Calculated new semver version: %s", new_version)
    return new_version
