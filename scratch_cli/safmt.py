# format sa objects
import scratchattach as sa
from scratch_cli import rfmt


def project(self: sa.Project):
    return rfmt.md_fp(
        "project.md",
        title=self.title,
        id=self.id,
        author=self.author_name,
    )
