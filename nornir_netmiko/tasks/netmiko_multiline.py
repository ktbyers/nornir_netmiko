from typing import Sequence, Union, List, Any
from nornir.core.task import Result, Task
from nornir_netmiko.connections import CONNECTION_NAME


def netmiko_multiline(
    task: Task,
    commands: Sequence[Union[str, List[str]]],
    use_timing: bool = False,
    enable: bool = False,
    **kwargs: Any
) -> Result:
    """
    Execute Netmiko send_multiline method (or send_multiline_timing)

    Arguments:
        commands: List or list of lists (see Netmiko send_multiline)
        use_timing: Set to True to switch to send_multiline_timing method.
        enable: Set to True to force Netmiko .enable() call.
        kwargs: Additional arguments to pass to send_multiline method.

    Returns:
        Result object with the following attributes set:
          * result: String result showing you the output from commands
    """
    net_connect = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    if enable:
        net_connect.enable()
    if use_timing:
        result = net_connect.send_multiline_timing(commands, **kwargs)
    else:
        result = net_connect.send_multiline(commands, **kwargs)
    return Result(host=task.host, result=result)
