from dataclasses import dataclass
from functools import cached_property

from src.integrations.structs import BaseTask


@dataclass
class JiraTask(BaseTask):
    @cached_property
    def _order_by_field(self) -> int:
        _, number = self.id.rsplit("-")
        return int(number)
