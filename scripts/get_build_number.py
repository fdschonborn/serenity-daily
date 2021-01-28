import os
from datetime import datetime

import requests

request_url = "https://api.github.com/repos/{}/tags?per_page=1&page=1".format(
    os.getenv("GITHUB_REPOSITORY", "fdschonborn/serenityos-daily"),
)

latest_tag = requests.get(request_url).json()[0]
latest_tag_name = latest_tag["name"]

print(f"Latest tag is:            {latest_tag}")

latest_tag_parts1 = latest_tag_name.split(".")       # ["v20210101", "0-blahbleh"]
latest_tag_parts2 = latest_tag_parts1[1].split("-")  # ["0", "blahbleh"]
latest_tag_date, latest_tag_build = str(latest_tag_parts1[0].lstrip("v")), int(latest_tag_parts2[0])

print(f"Latest release date is:   {latest_tag_date}")
print(f"Latest release build is:  {latest_tag_build}")

utcnow = datetime.utcnow()
current_date = f"{str(utcnow.year)[2:4]}{utcnow.month:02d}{utcnow.day:02d}"

current_build = 0
if latest_tag_date == current_date:
    current_build = latest_tag_build + 1

print(f"Current build number is:   {current_build}")
print(current_build, end='')
