# format sa objects
from typing import Optional, Iterable

from html import unescape

import scratchattach as sa
from scratch_cli import rfmt

from rich.color import Color
from scratch_cli.scli_config import scli_config
from scratch_cli.util import ERROR_MSG

RESET = "\x1b[0m"

def color(content: Optional[str], /):
    if content is None:
        return ''

    codes = Color.parse(content).get_ansi_codes()
    color_code = f"\x1b[{';'.join(codes)}m"
    return color_code

def color_all(content: str, color_str: Optional[str], /):
    """
    Prepend the color to every word to force colored printing. More chars means less space in the terminal, so be careful
    """
    _col = color(color_str)
    return _col + (' ' + _col).join(content.split()) + RESET

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

def project_page(self: sa.Project):
    # todo: allow for project-specific scli config

    return rfmt.md_fp(
        "project_page.md",
        title=rfmt.escape(self.title),
        author=rfmt.escape(self.author_name) if hasattr(self, "author_name") else None,
        id=self.id,
        instructions=rfmt.quote(_handle_configurable_markdownable(rfmt.escape(self.instructions), "", False)),
        notes=rfmt.quote(_handle_configurable_markdownable(rfmt.escape(self.notes), "", False)),
        views=self.views,
        loves=self.loves,
        faves=self.favorites,
        remix_count=self.remix_count,
        created=self.created,
        last_modified=self.last_modified,
        commenting_status="on" if self.comments_allowed else "off",
        remix_parent=self.remix_parent
    )

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
        color_data = ocular_data.get("color")
        if color_data is not None:
            color_str = f" {color(color_data)}⬤{RESET}"

        ocular = f"*{rfmt.escape(status)}*{color_str}"

    return rfmt.md_fp(
        "user_profile.md",

        username=rfmt.escape(self.name),
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


# noinspection PyUnresolvedReferences
def activity_raw(self: sa.Activity) -> list[str]:
    if isinstance(self.raw, str):
        return [self.raw]

    match self.type:
        case "loveproject":
            return [f"{self.actor_username}",  "loved", f"-P {self.title!r} ({self.project_id})"]
        case "favoriteproject":
            return [f"{self.actor_username}",  "favorited", f"-P {self.project_title!r} ({self.project_id})"]
        case "becomecurator":
            return [f"{self.actor_username}",  "now curating", f"-S {self.title!r} ({self.gallery_id})"]
        case "followuser":
            return [f"{self.actor_username}",  "followed", f"-U {self.followed_username}"]
        case "followstudio":
            return [f"{self.actor_username}",  "followed", f"-S {self.title!r} ({self.gallery_id})"]
        case "shareproject":
            return [f"{self.actor_username}",  "shared", f"-P {self.title!r} ({self.project_id})"]
        case "remixproject":
            return [f"{self.actor_username}",  "remixed", f"-P {self.parent_title!r} ({self.parent_id}) as -P {self.title!r} ({self.project_id})"]
        case "becomeownerstudio":
            return [f"{self.actor_username}",  "became owner of", f"-S {self.gallery_title!r} ({self.gallery_id})"]

        case "addcomment":
            ret = [self.actor_username, "commented on"]

            match self.comment_type:
                case 0:
                    # project
                    ret.append(f"-P {self.comment_obj_title!r} ({self.comment_obj_id}")
                case 1:
                    # user
                    ret.append(f"-U {self.comment_obj_title}")

                case 2:
                    # studio
                    ret.append(f"-S {self.comment_obj_title!r} ({self.comment_obj_id}")

                case _:
                    raise ValueError(f"Unknown comment type: {self.comment_type}")

            ret[-1] += f"#{self.comment_id})"

            ret.append(f"{unescape(self.comment_fragment)}")

            return ret

        case "curatorinvite":
            return [f"{self.actor_username}", "invited you to curate", f"-S {self.title!r} ({self.gallery_id})"]

        case "userjoin":
            return [f"{self.actor_username}", "joined Scratch"]

        case "studioactivity":
            return ['Studio activity', '', f"-S {self.title!r} ({self.gallery_id})"]

        case _:
            raise NotImplementedError(f"Activity type {self.type!r} is not implemented!\n"
                                      f"\n"
                                      f"{ERROR_MSG}")

# color, icon
ACTIVITY_TABLE = {
    "loveproject": ["red", "♥"],
    "favoriteproject": ["yellow", "★"],
    "becomecurator": ["green", "👥"],
    "followuser": ["blue", "👥"],
    "followstudio": ["blue", '👥'],
    "shareproject": ["orange1", "❏"],
    "remixproject": ["green", "꩜"],
    "becomeownerstudio": ["red", "👤"],
    "addcomment": ["blue", "💬"],
    "studioactivity": ["green", "❏"],
    "curatorinvite": ["green", "👥"],
    "userjoin": ["green", "👤"]
}

def activity_prettymsg(self: sa.Activity) -> str:
    raw = activity_raw(self)

    for i, item in enumerate(raw):
        raw[i] = rfmt.escape(item)

    raw.append(f"_{color('grey50')}{self.datetime_created}{RESET}_")

    activity_formatter = ACTIVITY_TABLE.get(self.type, [None, ''])
    code = color(activity_formatter[0])
    icon = activity_formatter[1]
    if icon:
        icon = f"{code}{icon}{RESET} "


    if len(raw) > 1 and raw[1]:
        raw[1] = f"{code}{raw[1]}{RESET}"

    if self.type == "addcomment":
        raw[3] = f"\n{rfmt.quote(raw[3])}\n"

    new = ' '.join(filter(lambda x: x, raw))

    return f"{icon}{new}"

def activity(self: sa.Activity):
    return rfmt.md_fp(
        "activity.md",
        msg=activity_prettymsg(self)
    )
