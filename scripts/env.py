#!/usr/bin/env python3
# env.py
# Fetch and parse the last release's tag name and create a new tag for the next
# release.

import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List

import requests


class Tag:
    date: str
    build: int
    commit: str

    def __init__(self, parts: List[str]):
        self.date = parts[0].lstrip("v")
        self.build = int(parts[1])
        self.commit = parts[2]

    def __str__(self) -> str:
        return f"{self.date}-{self.build}-{self.commit}"


response = requests.post(
    "https://api.github.com/graphql",
    json={
        "query": open(
            Path(__file__).parent / "releases.gql"
        ).read()
    },
    headers={
        "Authorization": "Bearer {}".format(
            os.getenv("GITHUB_TOKEN")
        )
    }).json()

tag = Tag(
    response
    ["data"]
    ["repository"]
    ["releases"]
    ["nodes"][0]
    ["tagName"].split("-")
)

now = datetime.utcnow().strftime("%y%m%d")
if tag.date == now:
    tag.build += 1
else:
    tag.date = now
    tag.build = 1

tag.commit = subprocess.check_output(
    [
        "git", "-C", os.getenv("SERENITY_ROOT", "serenity"),
        "rev-parse", "--short", "HEAD"
    ]
).strip().decode("utf-8")

with open(os.getenv("GITHUB_ENV", ".env"), "a") as github_env:
    def write_env(name: str, value: str):
        print(f"{name}={value}")
        github_env.write(f"{name}={value}\n")

    write_env("SERENITY_DAILY_DATE", tag.date)
    write_env("SERENITY_DAILY_BUILD", str(tag.build))
    write_env("SERENITY_DAILY_COMMIT", tag.commit)
