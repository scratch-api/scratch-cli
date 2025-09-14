import json

from typing import Optional

from scratch_cli.decorator import sessionable, EXIT_SESSION_LOOP

from scratch_cli.context import context
from scratch_cli.scli_config import scli_config_with_project, scli_config, scli_validator, generate_scli_config, \
    validate_scli_config_project_page, scli_config_project_id
from scratch_cli import rfmt, safmt
from scratch_cli import appdata
from scratch_cli import util

from scratch_cli.cmd.group import select_group_member

from scratchattach.utils import exceptions as sa_exceptions


@sessionable
def print_configs():
    user = context.session.connect_linked_user()
    data, project = scli_config_with_project(user)

    url = f" (https://scratch.mit.edu/projects/{project.id}/)" if project else ' (None)'

    rfmt.print_md(
        safmt.user(user) + f"""\
SCLI_CONFIG{url}:
```json
{json.dumps(data)}
```""")


def edit_config():
    session = context.session
    user = session.connect_linked_user()
    username = user.username

    data = scli_config(user)
    fp = (appdata.TEMP / "SCLI_CONFIG.json")
    json.dump(data, fp.open("w"))

    util.open_file(fp)
    input("Press Enter to continue...")
    data = json.load(fp.open())

    scli_validator.validate_python(data)
    print(f"Setting {username} to {data}")

    project_body = generate_scli_config(data)

    try:
        project = validate_scli_config_project_page(scli_config_project_id(user), username)
        print(project.set_json(project_body.to_json()))
    except (AssertionError, sa_exceptions.ProjectNotFound):
        project = session.create_project(
            title="_SCLI_CONFIG_",
            project_json=project_body.to_json()
        )
        project.share()

        appendix = f"\n{project.id}"
        user.set_bio(user.about_me[:200 - len(appendix)] + appendix)

    print(f"Sent to {project.url}")

    return EXIT_SESSION_LOOP


def config(command: Optional[str]):
    match command:
        case "edit":
            select_group_member()
            edit_config()

        case None:
            print_configs()
