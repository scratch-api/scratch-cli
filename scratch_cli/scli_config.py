import json
import warnings

from typing import TypedDict, NotRequired

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


def scli_config(self: sa.User) -> SCLIConfig:
    """
    Get and return SCLI config data, if any. If none, return empty dict.
    """
    about_me, project_id = split_trailing_number(self.about_me)
    if not project_id:
        return {}

    # project id may be valid, it may be not
    try:
        _project = context.session.connect_project(project_id)
    except sa_exceptions.ProjectNotFound:
        return {}

    if _project.title != "_SCLI_CONFIG_":
        return {}
    if _project.author_name.lower() != self.username.lower():
        return {}

    _project_body = editor.Project.from_json(_project.raw_json())
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


def generate_scli_config(data: SCLIConfig):
    scli_validator.validate_python(data)

    stage = editor.Sprite(True, "_stage_")
    project = editor.Project("_SCLI_CONFIG_", _sprites=[stage])

    stage.add_comment(editor.Comment(
        stage.new_id,
        text=f"{json.dumps(data)}\n_SCLI_CONFIG_",
    ))

    stage.costumes.append(editor.Costume())

    return project


if __name__ == '__main__':
    print(split_trailing_number("Browsing scratch in a terminal, far, far away...\n\n\n\n1216591875"))

    print(generate_scli_config({
                             'test': "This is verified by pydantic. It's also the only key where you're allowed to put anything you want, so long as it's a string.",
                             'profile': {'about_me': {'content': 'Idk', 'replace': True}}}))
