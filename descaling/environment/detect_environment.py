import dataclasses
import platform

import enum
import os
from typing import Optional
import sh


class OperatingSystem(enum.Enum):
    Windows = "windows"
    Linux = "linux"
    Darwin = "darwin"


class SessionType(enum.Enum):
    X11 = "x11"
    Wayland = "wayland"


@dataclasses.dataclass
class Environment:
    operating_system: OperatingSystem
    session_type: Optional[SessionType]


def detect_session_type() -> Optional[SessionType]:
    if "XDG_SESSION_TYPE" in os.environ:
        session = os.environ.get("XDG_SESSION_TYPE")

        if session == "x11":
            return SessionType.X11
        elif session == "wayland":
            return SessionType.Wayland

    session = sh.loginctl(
        "show-session",
        sh.loginctl(
            "show-user",
            sh.whoami().replace("\n", ""),
            p="Display",
            value=True
        ).replace("\n", ""),
        p="Type",
        value=True
    )

    if session == "x11":
        return SessionType.X11
    elif session == "wayland":
        return SessionType.Wayland


def detect_operating_system() -> OperatingSystem:
    operating_system = platform.system()

    if operating_system == "Linux":
        return OperatingSystem.Linux
    elif operating_system == "Windows":
        return OperatingSystem.Windows
    elif operating_system == "Darwin":
        return OperatingSystem.Darwin