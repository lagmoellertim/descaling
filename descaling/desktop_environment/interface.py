import abc
from abc import ABC, abstractmethod


class DesktopEnvironmentInterface(ABC):
    name: str

    @staticmethod
    @abstractmethod
    def is_current_desktop_environment() -> bool:
        pass

    @staticmethod
    @abstractmethod
    def pre_xrandr_hook(scaling: float):
        pass

    @staticmethod
    @abstractmethod
    def post_xrandr_hook(scaling: float):
        pass

    @staticmethod
    @abstractmethod
    def get_ui_scaling() -> float:
        pass
