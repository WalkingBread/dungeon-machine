from dataclasses import dataclass
import logic.modelmanager.configured.models as models

@dataclass
class GameEvent:
    event: models.GameEvent
    
    def to_dict(self) -> dict: 
        return {
            'type': str(self.event)
        }