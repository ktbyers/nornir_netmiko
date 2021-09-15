from typing import Any
from nornir.core.task import Result, Task
from nornir_netmiko.connections import CONNECTION_NAME


def netmiko_commit(task: Task, **kwargs: Any) -> Result:
    """
    Execute Netmiko commit method

    Arguments:
        kwargs: Additional arguments to pass to method.

    Returns:
        :obj: `nornir.core.task.Result`:
          * result (``str``): String showing the CLI output from the commit operation
    """
    conn = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    result = conn.commit(**kwargs)

    if conn.check_config_mode():
        conn.exit_config_mode()
    return Result(host=task.host, result=result, changed=True)
