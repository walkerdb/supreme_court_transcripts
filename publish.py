#!/usr/bin/env python3

from datetime import date
from os import environ
import requests

MAX_NUM_RELEASES = 3

repo = environ.get("GITHUB_REPOSITORY")
url = f"https://api.github.com/repos/{repo}/releases"

token = environ.get("GITHUB_TOKEN")
assert token, "GITHUB_TOKEN not found"
headers = {"Authorization": f"Bearer {token}"}

## Clean up old releases

resp = requests.get(url, headers=headers)
resp.raise_for_status()
releases = resp.json()

if len(releases) >= MAX_NUM_RELEASES:
    # we assumed older releases are later in the list
    to_delete = releases[MAX_NUM_RELEASES - 1 :]
    for release in to_delete:
        delete_url = url + f"/{release['id']}"
        delete_resp = requests.delete(delete_url, headers=headers)
        delete_resp.raise_for_status()
        print(delete_resp)


## Create a new release
date_str = str(date.today())
release_request = {
    "tag_name": date_str,
    "target_commitish": "master",
    "name": date_str,
    "body": f"Updated on {date_str}",
}

resp = requests.post(url, json=release_request, headers=headers)
print(resp)
resp.raise_for_status()
