from typing import Callable, Optional
from dataclasses import dataclass

INFINITE_DURATION = -1


@dataclass
class Status:
    name: str
    duration: int
    stackable: bool = True
    on_turn: Optional[Callable] = None
    on_apply: Optional[Callable] = None
    on_remove: Optional[Callable] = None

    def __hash__(self) -> int:
        if self.stackable:
            return hash((self.name,self.duration))
        return hash(self.name)
    
    def __eq__(self, other):
        if not isinstance(other, Status):
            return False
        if self.stackable:
            return (self.name, self.duration) == (other.name, other.duration)
        return self.name == other.name
    