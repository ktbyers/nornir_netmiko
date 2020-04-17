from nornir_napalm.tasks.napalm_cli import napalm_cli
from nornir_napalm.tasks.napalm_configure import napalm_configure
from nornir_napalm.tasks.napalm_get import napalm_get
from nornir_napalm.tasks.napalm_ping import napalm_ping
from nornir_napalm.tasks.napalm_validate import napalm_validate


__all__ = (
    "napalm_cli",
    "napalm_configure",
    "napalm_get",
    "napalm_ping",
    "napalm_validate",
)
