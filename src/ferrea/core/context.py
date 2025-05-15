from dataclasses import dataclass


@dataclass
class Context:
    uuid: str
    app: str

    @property
    def log(self) -> dict[str, str]:
        """Log the context"""
        return {"ferrea_uuid": self.uuid, "app": self.app}
