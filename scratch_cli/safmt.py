# format sa objects
from typing import Optional, Iterable

import scratchattach as sa
from scratch_cli import rfmt

from rich.color import Color
from scratch_cli.scli_config import scli_config

RESET = "\x1b[0m"


def collate(func, for_objs: Iterable) -> str:
    return '\n'.join(func(obj) for obj in for_objs)


def project(self: sa.Project):
    return rfmt.md_fp(
        "project.md",
        title=self.title,
        id=self.id,
        author=self.author_name if hasattr(self, "author_name") else None,
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


def user(self: sa.User):
    return rfmt.md_fp(
        "user.md",
        username=self.name,
        id=self.id,
    )


def _handle_configurable_markdownable(raw: str, content: Optional[str], replace: bool,
                                      splitter: str = '\n\n---\n\n') -> str:
    if content:
        if replace:
            return content
        else:
            return f'{raw}{splitter}{content}'
    return raw


def user_profile(self: sa.User):
    config = scli_config(self)
    config_profile = config.get("profile", {})

    # handle bio and wiwo
    wiwo = rfmt.escape(self.wiwo)

    config_about_me = config_profile.get("about_me", {})
    about_me_raw = _handle_configurable_markdownable(
        rfmt.escape(self.about_me),
        config_about_me.get("content"),
        config_about_me.get("replace", True))

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
        rank=user_rank(self),
        country=self.country,
        ocular=ocular,
        join_date=self.join_date,
        about_me=rfmt.quote(about_me_raw),
        wiwo=rfmt.quote(wiwo),
        message_count=self.message_count(),
        featured=featured_project(self.featured_data())
    )

def user_rank(self: sa.User):
    if self.scratchteam:
        return "Scratch Team"
    status = self.is_new_scratcher()

    if status is None:
        return "Unknown"

    if status:
        return "New scratcher"
    else:
        return "Scratcher"
