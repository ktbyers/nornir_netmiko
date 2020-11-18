from typing import Any
from nornir.core.task import Result, Task
from nornir_netmiko.connections import CONNECTION_NAME


def netmiko_send_command(
    task: Task,
    command_string: str,
    use_timing: bool = False,
    enable: bool = False,
    config_mode=False,
    config_command=None,
    **kwargs: Any
) -> Result:
    """
    Execute Netmiko send_command method (or send_command_timing)

    Arguments:
        command_string: Command to execute on the remote network device.
        use_timing: Set to True to switch to send_command_timing method.
        enable: Set to True to force Netmiko .enable() call.
        kwargs: Additional arguments to pass to send_command method.

    Returns:
        Result object with the following attributes set:
          * result: Result of the show command (generally a string, but depends on use of TextFSM).
    """
    net_connect = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    if enable:
        net_connect.enable()
    if config_mode:
        cfg_mode_args = (config_command,) if config_command else tuple()
        net_connect.config_mode(*cfg_mode_args)
    if use_timing:
        result = net_connect.send_command_timing(command_string, **kwargs)
    else:
        result = net_connect.send_command(command_string, **kwargs)
    return Result(host=task.host, result=result)
