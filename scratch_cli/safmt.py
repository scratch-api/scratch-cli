# format sa objects
from typing import Optional

import scratchattach as sa
from scratch_cli import rfmt

from rich.color import Color

RESET = "\x1b[0m"


def project(self: sa.Project):
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
    ocular_data = self.ocular_status()
    ocular = 'No ocular status'

    if status := ocular_data.get("status"):
        color = ocular_data.get("color")
        codes = Color.parse(color).get_ansi_codes()
        color_code = f"\x1b[{';'.join(codes)}m"

        ocular = f"*{status}* {color_code}⬤{RESET}"

    return rfmt.md_fp(
        "user_profile.md",

        username=self.name,
        id=self.id,
        rank="Scratch Team" if self.scratchteam else ["Scratcher", "New scratcher"][
            self.is_new_scratcher()],
        country=self.country,
        ocular=ocular,
        join_date=self.join_date,
        about_me=rfmt.quote(self.about_me),
        wiwo=rfmt.quote(self.wiwo),
        message_count=self.message_count(),
        featured=featured_project(self.featured_data())
    )
