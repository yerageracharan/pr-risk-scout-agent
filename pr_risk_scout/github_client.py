import requests

def fetch_pull_request_diff(repository, pull_number, token=None):
    if repository.count("/") != 1:
        raise ValueError("Repository must be owner/name")
    url = f"https://api.github.com/repos/{repository}/pulls/{pull_number}"
    headers = {
        "Accept": "application/vnd.github.v3.diff",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "pr-risk-scout-agent",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.text
