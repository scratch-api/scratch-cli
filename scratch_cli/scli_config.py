import json
import warnings

from typing import TypedDict, NotRequired, Optional

import scratchattach as sa
from scratchattach import editor
from scratchattach.utils import exceptions as sa_exceptions
from scratch_cli.context import context
from scratch_cli.util import split_trailing_number

import pydantic


class InputSettings(TypedDict):
    content: str
    replace: bool


class Profile(TypedDict):
    about_me: NotRequired[InputSettings]
    wiwo: NotRequired[InputSettings]


class SCLIConfig(TypedDict):
    test: NotRequired[str]
    profile: NotRequired[Profile]


scli_validator = pydantic.TypeAdapter(SCLIConfig)


def scli_config_project_id(self: sa.User) -> Optional[int]:
    about_me, project_id = split_trailing_number(self.about_me)
    return project_id if project_id else None


def validate_scli_config_project_page(project_id: Optional[int], username: str):
    assert project_id is not None

    # project id may be valid, it may be not
    _project = context.session.connect_project(project_id)

    assert _project.title.startswith("_SCLI_CONFIG_")

    assert _project.author_name.lower() == username.lower()

    return _project


def scli_config_from_project(self: sa.Project) -> SCLIConfig:
    _project_body = editor.Project.from_json(self.raw_json())
    _possible_comments = _project_body.stage.comments

    if len(_possible_comments) != 1:
        return {}

    _comment = _possible_comments[0].text

    if not _comment.endswith("_SCLI_CONFIG_"):
        return {}

    _comment = _comment[:-len("_SCLI_CONFIG_")]

    try:
        data = json.loads(_comment)

    except json.decoder.JSONDecodeError:
        warnings.warn(f"Could not decode SCLI comment: {_comment=}")
        return {}

    try:
        return scli_validator.validate_python(data)
    except pydantic.ValidationError:
        warnings.warn(f"Invalid SCLI comment: {_comment=}")
        return {}

def scli_config_with_project(self: sa.User) -> tuple[SCLIConfig, Optional[sa.Project]]:
    project_id = scli_config_project_id(self)
    if not project_id:
        return SCLIConfig(), None
    try:
        _project = validate_scli_config_project_page(project_id, self.username)
    except (AssertionError, sa_exceptions.ProjectNotFound):
        return SCLIConfig(), None

    return scli_config_from_project(_project), _project

def scli_config(self: sa.User) -> SCLIConfig:
    """
    Get and return SCLI config data, if any. If none, return empty dict.
    """
    return scli_config_with_project(self)[0]

def generate_scli_config(data: SCLIConfig):
    scli_validator.validate_python(data)

    stage = editor.Sprite(True, "Stage", _layer_order=0)
    project = editor.Project("_SCLI_CONFIG_", _sprites=[stage])

    stage.add_comment(editor.Comment(
        stage.new_id,
        text=f"{json.dumps(data)}\n_SCLI_CONFIG_",
    ))

    stage.costumes.append(cost := editor.Costume(bitmap_resolution=0))
    cost.sprite = stage

    return project


if __name__ == '__main__':
    print(split_trailing_number("Browsing scratch in a terminal, far, far away...\n\n\n\n1216591875"))

    print(generate_scli_config({
        'test': "This is verified by pydantic. It's also the only key where you're allowed to put anything you want, so long as it's a string.",
        'profile': {'about_me': {'content': 'Idk', 'replace': True}}}))
