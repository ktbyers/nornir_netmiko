from typing import Any, Dict, Optional

from netmiko import SSHDetect
from netmiko import ConnectHandler

from nornir.core.configuration import Config


CONNECTION_NAME = "netmiko"

napalm_to_netmiko_map = {
    "ios": "cisco_ios",
    "nxos": "cisco_nxos",
    "nxos_ssh": "cisco_nxos",
    "eos": "arista_eos",
    "junos": "juniper_junos",
    "iosxr": "cisco_xr",
    "netmiko_auto":"autodetect"
}


class Netmiko:
    """
    This plugin connects to the device using the Netmiko driver and sets the
    relevant connection.
    Inventory:
        extras: maps to argument passed to ``ConnectHandler``.
    """

    def open(
        self,
        hostname: Optional[str],
        username: Optional[str],
        password: Optional[str],
        port: Optional[int],
        platform: Optional[str],
        extras: Optional[Dict[str, Any]] = None,
        configuration: Optional[Config] = None,
    ) -> None:
        parameters = {
            "host": hostname,
            "username": username,
            "password": password,
            "port": port,
        }

        try:
            parameters[
                "ssh_config_file"
            ] = configuration.ssh.config_file  # type: ignore
        except AttributeError:
            pass

        if platform is not None:
            # Look platform up in corresponding map, if no entry return the host.nos unmodified
            platform = napalm_to_netmiko_map.get(platform, platform)
            if platform ==  "autodetect":# If we are using autodect
                parameters["device_type"] = platform
                connection = ConnectHandler(**parameters)
                best_match = guesser.autodetect()
                if best_match: # If we find a device_type
                    parameters['device_type'] = best_match
                else:
                    raise ValueError("Netmiko cannot detect the device_type")
            parameters["device_type"] = platform

        extras = extras or {}
        parameters.update(extras)
        connection = ConnectHandler(**parameters)
        self.connection = connection

    def close(self) -> None:
        self.connection.disconnect()
