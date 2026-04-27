import base64
import requests
import re
import time
import urllib.parse
import yaml
from bs4 import BeautifulSoup

FTS_CONFIG = {
    # table: columns
    "commits": ["message"],
    "issue_comments": ["body"],
    "issues": ["title", "body"],
    "pull_requests": ["title", "body"],
    "labels": ["name", "description"],
    "licenses": ["name"],
    "milestones": ["title", "description"],
    "releases": ["name", "body"],
    "repos": ["name", "description"],
    "users": ["login", "name"],
}

VIEWS = {
    # Name: (required_tables, SQL)
    "dependent_repos": (
        {"repos", "dependents"},
        """select
  repos.full_name as repo,
  'https://github.com/' || dependent_repos.full_name as dependent,
  dependent_repos.created_at as dependent_created,
  dependent_repos.updated_at as dependent_updated,
  dependent_repos.stargazers_count as dependent_stars,
  dependent_repos.watchers_count as dependent_watchers
from
  dependents
  join repos as dependent_repos on dependents.dependent = dependent_repos.id
  join repos on dependents.repo = repos.id
order by
  dependent_repos.created_at desc""",
    ),
    "repos_starred": (
        {"stars", "repos", "users"},
        """select
  stars.starred_at,
  starring_user.login as starred_by,
  repos.*
from
  repos
  join stars on repos.id = stars.repo
  join users as starring_user on stars.user = starring_user.id
  join users on repos.owner = users.id
order by
  starred_at desc""",
    ),
    "recent_releases": (
        {"repos", "releases"},
        """select
  repos.rowid as rowid,
  repos.html_url as repo,
  releases.html_url as release,
  substr(releases.published_at, 0, 11) as date,
  releases.body as body_markdown,
  releases.published_at,
  coalesce(repos.topics, '[]') as topics
from
  releases
  join repos on repos.id = releases.repo
order by
  releases.published_at desc""",
    ),
}

FOREIGN_KEYS = [
    ("repos", "license", "licenses", "key"),
]


class GitHubError(Exception):
    def __init__(self, message, status_code, headers=None):
        self.message = message
        self.status_code = status_code
        self.headers = headers



class GitHubRepositoryEmpty(GitHubError):
    pass






























































def ensure_db_shape(db):
    "Ensure FTS is configured and expected FKS, views and (soon) indexes are present"
    pass












_href_re = re.compile(r'\shref="#([^"]+)"')
_id_re = re.compile(r'\sid="([^"]+)"')






