import argparse
from typing import Literal, Optional

class Args(argparse.Namespace):
    command: Literal['login', 'group', 'groups', 'ungroup', 'profile', 'find', 'config', None]
    username: Optional[str]

    # find
    offset: int
    limit: int
    mode: Optional[str]

    # login
    login_by_sessid: bool

    # group
    group_command: Literal['switch', 'rename', 'delete', None]
    name: Optional[str]

    # config
    config_command: Optional[str]
