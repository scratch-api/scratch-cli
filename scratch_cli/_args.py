import argparse
from typing import Literal, Optional

class Args(argparse.Namespace):
    command: Literal['login', 'group', 'groups', 'ungroup', 'profile', 'find', 'config', None]

    # find
    offset: int
    limit: int
    user: Optional[str]
    mode: Optional[str]

    # login
    login_by_sessid: bool = False

    # group
    group_command: Literal['switch', 'rename', 'delete', None]
    name: Optional[str]

    # config
    config_command: Optional[str]
