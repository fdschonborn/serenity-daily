import os
from datetime import datetime

import requests

repo = os.getenv("GITHUB_REPOSITORY", "fdschonborn/serenityos-daily")
request_url = f"https://api.github.com/repos/{repo}/tags"
last_tag = requests.get(request_url).json()[0]["name"]
parts1 = last_tag.split(".")
parts2 = parts1[1].split("-")
last_date, last_build = parts1[0].lstrip("v"), int(parts2[0])

utcnow = datetime.utcnow()
now_date = f"{utcnow.year:04d}{utcnow.month:02d}{utcnow.day:02d}"

new_build = 0
if last_date == now_date:
    new_build = last_build + 1

print(new_build, end='')
