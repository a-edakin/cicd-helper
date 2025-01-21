from dataclasses import dataclass

from git import Commit


@dataclass
class BaseTask:
    id: str
    name: str
    done: bool

    @property
    def _order_by_field(self) -> int:
        raise NotImplementedError("_order_by_field is not implemented.")

    def __lt__(self, other):
        return self._order_by_field < other._order_by_field

    def __le__(self, other):
        return self._order_by_field <= other._order_by_field

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __gt__(self, other):
        return self._order_by_field > other._order_by_field

    def __ge__(self, other):
        return self._order_by_field >= other._order_by_field


@dataclass
class ToDo:
    commit: Commit
    text: str

    @property
    def short(self) -> str:
        return f"{self.text[:40]}..."
