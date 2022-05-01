from typing import Optional

from .desktop_environment import DesktopEnvironmentInterface, desktop_environment_collection
from .environment import OperatingSystem, detect_operating_system, detect_session_type, SessionType


def get_desktop_environment() -> Optional[DesktopEnvironmentInterface]:
    if (operating_system := detect_operating_system()) != OperatingSystem.Linux:
        raise EnvironmentError(f"This library only supports Linux, {operating_system} was found.")

    if (session_type := detect_session_type()) != SessionType.X11:
        raise EnvironmentError(f"This library only supports x11, {session_type} was found")

    for desktop_environment in desktop_environment_collection:
        if desktop_environment.is_current_desktop_environment():
            return desktop_environment

    raise EnvironmentError(f"The current desktop environment is not supported")
