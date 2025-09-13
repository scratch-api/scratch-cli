# format sa objects
import json
import warnings

from typing import Optional, Iterable, TypedDict, NotRequired

import scratchattach as sa
from scratchattach import editor
from scratchattach.utils import exceptions as sa_exceptions
from scratch_cli import rfmt
from scratch_cli.context import context

from rich.color import Color

import pydantic

RESET = "\x1b[0m"

def split_trailing_number(self: str) -> tuple[str, str]:
    number = ""
    while len(self) and self[-1].isnumeric():
        number = self[-1] + number
        self = self[:-1]

    return self, number

class SCLIConfig(TypedDict):
    test: NotRequired[str]

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

    scli_validator = pydantic.TypeAdapter(SCLIConfig)

    try:
        return scli_validator.validate_python(data)
    except pydantic.ValidationError:
        warnings.warn(f"Invalid SCLI comment: {_comment=}")
        return {}

def collate(func, for_objs: Iterable) -> str:
    return '\n'.join(func(obj) for obj in for_objs)

def project(self: sa.Project):
    if not hasattr(self, "author_name"):
        self.update()

    return rfmt.md_fp(
        "project.md",
        title=self.title,
        id=self.id,
        author=self.author_name,
    )


def featured_project(self: Optional[dict[str, str | dict[str, str]]]):
    if not self:
        self = {}
    self_project = self.get("project", {})

    return rfmt.md_fp(
        "featured_project.md",
        heading=self.get("label", "Featured Project"),
        title=self_project.get("title"),
        id=self_project.get("id")
    ) if self else '###### No featured project'


def user_profile(self: sa.User):
    print(scli_config(self))

    ocular_data = self.ocular_status()
    ocular = 'No ocular status'

    if status := ocular_data.get("status"):
        color_str = ''
        color = ocular_data.get("color")
        if color is not None:
            codes = Color.parse(color).get_ansi_codes()
            color_code = f"\x1b[{';'.join(codes)}m"
            color_str = f" {color_code}⬤{RESET}"

        ocular = f"*{status}*{color_str}"

    return rfmt.md_fp(
        "user_profile.md",

        username=self.name,
        id=self.id,
        rank="Scratch Team" if self.scratchteam else ["Scratcher", "New scratcher"][
            self.is_new_scratcher()],
        country=self.country,
        ocular=ocular,
        join_date=self.join_date,
        about_me=rfmt.quote(rfmt.escape(self.about_me)),
        wiwo=rfmt.quote(rfmt.escape(self.wiwo)),
        message_count=self.message_count(),
        featured=featured_project(self.featured_data())
    )

if __name__ == '__main__':
    print(split_trailing_number("Browsing scratch in a terminal, far, far away...\n\n\n\n1216591875"))
