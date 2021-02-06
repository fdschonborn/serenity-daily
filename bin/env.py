import subprocess
import os
from datetime import datetime

import requests


class Tag:
    date: str
    build: int
    commit: str

    def __init__(self, parts: list[str]):
        self.date = parts[0].lstrip("v")
        self.build = int(parts[1])
        self.commit = parts[2]

    def __str__(self) -> str:
        return f"{self.date}-{self.build}-{self.commit}"


# TODO: We are requesting the second tag because the GitHub API won't sort tags
# by date but alphabetically, maybe we can try using the GraphQL API where we
# can request that sorting.
request_url = "https://api.github.com/repos/{}/tags?per_page=2&page=1".format(
    os.getenv("GITHUB_REPOSITORY", "fdschonborn/serenity-daily"),
)
tag = Tag(requests.get(request_url).json()[1]["name"].split("-"))  # NOTE: Ugly.

now = datetime.utcnow().strftime("%y%m%d")
if tag.date == now:
    tag.build += 1
else:
    tag.date = now
    tag.build = 0

tag.commit = subprocess.check_output(["git", "-C", os.getenv("SERENITY_ROOT", "serenity"),
                                      "rev-parse", "--short", "HEAD"]).strip().decode("utf-8")

with open(os.getenv("GITHUB_ENV", ".env"), "a") as github_env:
    def write_env(name: str, value: str):
        print(f"{name}=\"{value}\"")
        github_env.write(f"{name}=\"{value}\"\n")

    write_env("SERENITY_DAILY_DATE", tag.date)
    write_env("SERENITY_DAILY_BUILD", str(tag.build))
    write_env("SERENITY_DAILY_COMMIT", tag.commit)
