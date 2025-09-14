import argparse
from typing import Literal, Optional

class Args(argparse.Namespace):
    command: Literal['login', 'group', 'groups', 'ungroup', 'profile', 'find', 'config', None]

    username: Optional[str]
    project_id: Optional[int]

    mode: Optional[str]
    offset: int
    limit: int

    # login
    login_by_sessid: bool

    # group
    group_command: Literal['switch', 'rename', 'delete', None]
    name: Optional[str]

    # config
    config_command: Optional[str]
