import json
import os
import re

from descaling.desktop_environment.interface import DesktopEnvironmentInterface
import sh


class Gnome(DesktopEnvironmentInterface):
    name = "gnome"

    @staticmethod
    def is_current_desktop_environment() -> bool:
        if os.environ.get("DESKTOP_SESSION") == "gnome":
            return True

        if os.environ.get("XDG_SESSION_DESKTOP") == "gnome":
            return True

        return False

    @staticmethod
    def pre_xrandr_hook(scaling: float):
        sh.gsettings(
            "set", "org.gnome.desktop.interface",
            "scaling-factor", int(scaling)
        )

        sh.gsettings(
            "set", "org.gnome.settings-daemon.plugins.xsettings",
            "overrides", f"{{'Gdk/WindowScalingFactor': <{int(scaling)}>}}"
        )

    @staticmethod
    def post_xrandr_hook(scaling: float):
        pass

    @staticmethod
    def get_ui_scaling() -> float:
        scaling = float(str(sh.gsettings("get", "org.gnome.desktop.interface", "scaling-factor")).split(" ")[1])

        result = re.findall(
            r"Gdk\/WindowScalingFactor[\'\"]\W*:\W*<(\d*)>",
            str(sh.gsettings("get", "org.gnome.settings-daemon.plugins.xsettings", "overrides"))
        )

        if len(result) > 0:
            scaling = max(scaling, float(result[0]))

        return scaling