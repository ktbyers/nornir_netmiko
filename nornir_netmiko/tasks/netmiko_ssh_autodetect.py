from netmiko import NetmikoAuthenticationException, NetmikoTimeoutException
from netmiko.ssh_autodetect import SSHDetect
from nornir.core.task import Task, Result

def netmiko_ssh_autodetect(task: Task, update_platform : bool = False) -> Result:
    """ Uses Netmiko guesser to determine device type
    
    Arguments:
        update_platform: Update host.platform with best guess (default False)

    Returns:
        Result object with the following attributes set:
          * result (``str``): string with guessed operating system
          * changed (``bool``): always False.
          * failed (``bool``): True if any Netmiko Exception occurs
    
    """
    connection = {
        "host"       : task.host.hostname,
        "username"   : task.host.username,
        "password"   : task.host.password,
        "port"       : task.host.port,
        "device_type": 'autodetect'
    }

    try:
        guesser = SSHDetect(**connection)
        best_match = guesser.autodetect()
    except (NetmikoAuthenticationException, NetmikoTimeoutException):
        return Result(
            host=task.host,
            changed=True,
            failed=True,)

    # Updates the current host's platform. Useful if this task 
    # is the first one in a sequence of network mapping tasks
    # that require host.platform to be set later on.
    if update_platform:
        task.host.platform = best_match

    return Result(
        host=task.host,
        result=best_match,
        changed= False
    )
