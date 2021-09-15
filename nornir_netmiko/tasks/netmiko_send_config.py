from typing import Any, List, Optional
from nornir.core.task import Result, Task
from nornir_netmiko.connections import CONNECTION_NAME


def netmiko_send_config(
    task: Task,
    config_commands: Optional[List[str]] = None,
    config_file: Optional[str] = None,
    enable: bool = True,
    dry_run: Optional[bool] = None,
    **kwargs: Any
) -> Result:
    """
    Execute Netmiko send_config_set method (or send_config_from_file)

    Arguments:
        config_commands: Commands to configure on the remote network device.
        config_file: File to read configuration commands from.
        enable: Attempt to enter enable-mode.
        dry_run: Whether to apply changes or not (will raise exception)
        kwargs: Additional arguments to pass to method.

    Returns:
        Result object with the following attributes set:
          * result (``str``): string showing the CLI from the configuration changes.
    """
    net_connect = task.host.get_connection(CONNECTION_NAME, task.nornir.config)

    # netmiko_send_config does not support dry_run
    dry_run = task.is_dry_run(dry_run)
    if dry_run is True:
        raise ValueError("netmiko_send_config does not support dry_run")

    if enable:
        net_connect.enable()
    if config_commands:
        result = net_connect.send_config_set(config_commands=config_commands, **kwargs)
    elif config_file:
        result = net_connect.send_config_from_file(config_file=config_file, **kwargs)
    else:
        raise ValueError("Must specify either config_commands or config_file")

    return Result(host=task.host, result=result, changed=True)
