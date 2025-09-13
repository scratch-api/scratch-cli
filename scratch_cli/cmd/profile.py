from scratch_cli.decorator import sessionable
from scratch_cli.context import context
from scratch_cli import assets

import rich
from rich.markdown import Markdown
from rich.color import Color

RESET = "\x1b[0m"


@sessionable
def profile():
    user = context.session.connect_linked_user()
    ocular_data = user.ocular_status()
    ocular = 'No ocular status'

    if status := ocular_data.get("status"):
        color = ocular_data.get("color")
        codes = Color.parse(color).get_ansi_codes()
        color_code = f"\x1b[{';'.join(codes)}m"

        ocular = f"*{status}* {color_code}⬤{RESET}"

    featured_data = user.featured_data()
    if not featured_data:
        featured_data = {}
    featured_project = featured_data.get("project", {})

    assets.print_fmt(
        "user_profile.md",
        username=user.name,
        id=user.id,
        rank="Scratch Team" if user.scratchteam else ["Scratcher", "New scratcher"][
            user.is_new_scratcher()],
        country=user.country,
        ocular=ocular,
        join_date=user.join_date,
        about_me=user.about_me,
        wiwo=user.wiwo,
        message_count=user.message_count(),
        featured=assets.markdown_fmt(
            "featured_project.md",
            heading=featured_data.get("label", "Featured Project"),
            title=featured_project.get("title"),
            id=featured_project.get("id")
        ) if featured_data else '###### No featured project',
    )
