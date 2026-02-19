from abc import ABC, abstractmethod


class Agent(ABC):
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def run(self, user_input: str, history: list[tuple[str, str]] = None) -> dict:
        pass
