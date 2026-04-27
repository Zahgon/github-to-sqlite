import click
import datetime
import itertools
import pathlib
import textwrap
import os
import sqlite_utils
import time
import json
import bs4
from github_to_sqlite import utils


@click.group()
@click.version_option()
def cli():
    "Save data from GitHub to a SQLite database"


@cli.command()
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    default="auth.json",
    help="Path to save tokens to, defaults to auth.json",
)
def auth(auth):
    "Save authentication credentials to a JSON file"
    pass


@cli.command()
@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.argument("repo")
@click.option(
    "--issue",
    "issue_ids",
    help="Just pull these issue numbers",
    type=int,
    multiple=True,
)
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=True),
    default="auth.json",
    help="Path to auth.json token file",
)
@click.option(
    "--load",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=True, exists=True),
    help="Load issues JSON from this file instead of the API",
)
def issues(db_path, repo, issue_ids, auth, load):
    "Save issues for a specified repository, e.g. simonw/datasette"
    pass


@cli.command(name="pull-requests")
@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.argument("repo", required=False)
@click.option(
    "--pull-request",
    "pull_request_ids",
    help="Just pull these pull-request numbers",
    type=int,
    multiple=True,
)
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=True),
    default="auth.json",
    help="Path to auth.json token file",
)
@click.option(
    "--load",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=True, exists=True),
    help="Load pull-requests JSON from this file instead of the API",
)
@click.option(
    "--org",
    "orgs",
    help="Fetch all pull requests from this GitHub organization",
    multiple=True,
)
@click.option(
    "--state",
    help="Only fetch pull requests in this state",
)
@click.option(
    "--search",
    help="Find pull requests with a search query",
)
def pull_requests(db_path, repo, pull_request_ids, auth, load, orgs, state, search):
    "Save pull_requests for a specified repository, e.g. simonw/datasette"
    pass


@cli.command(name="issue-comments")
@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.argument("repo")
@click.option("--issue", help="Just pull comments for this issue")
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=True),
    default="auth.json",
    help="Path to auth.json token file",
)
def issue_comments(db_path, repo, issue, auth):
    "Retrieve issue comments for a specific repository"
    pass


@cli.command()
@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.argument("username", type=str, required=False)
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=True),
    default="auth.json",
    help="Path to auth.json token file",
)
@click.option(
    "--load",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=True, exists=True),
    help="Load issues JSON from this file instead of the API",
)
def starred(db_path, username, auth, load):
    "Save repos starred by the specified (or authenticated) username"
    pass


@cli.command()
@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.argument("repos", type=str, nargs=-1)
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=True),
    default="auth.json",
    help="Path to auth.json token file",
)
def stargazers(db_path, repos, auth):
    "Fetch the users that have starred the specified repositories"
    pass


@cli.command()
@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.argument("usernames", type=str, nargs=-1)
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=True),
    default="auth.json",
    help="Path to auth.json token file",
)
@click.option(
    "-r",
    "--repo",
    multiple=True,
    help="Just fetch these repos",
)
@click.option(
    "--load",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=True, exists=True),
    help="Load repos JSON from this file instead of the API",
)
@click.option(
    "--readme",
    is_flag=True,
    help="Fetch README into 'readme' column",
)
@click.option(
    "--readme-html",
    is_flag=True,
    help="Fetch HTML rendered README into 'readme_html' column",
)
def repos(db_path, usernames, auth, repo, load, readme, readme_html):
    "Save repos owned by the specified (or authenticated) username or organization"
    pass




@cli.command()
@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.argument("repos", type=str, nargs=-1)
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=True),
    default="auth.json",
    help="Path to auth.json token file",
)
def releases(db_path, repos, auth):
    "Save releases for the specified repos"
    pass


@cli.command()
@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.argument("repos", type=str, nargs=-1)
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=True),
    default="auth.json",
    help="Path to auth.json token file",
)
def tags(db_path, repos, auth):
    "Save tags for the specified repos"
    pass


@cli.command()
@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.argument("repos", type=str, nargs=-1)
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=True),
    default="auth.json",
    help="Path to auth.json token file",
)
def contributors(db_path, repos, auth):
    "Save contributors for the specified repos"
    pass


@cli.command()
@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.argument("repos", type=str, nargs=-1)
@click.option(
    "--all",
    is_flag=True,
    default=False,
    help="Load all commits (not just those that have not yet been saved)",
)
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=True),
    default="auth.json",
    help="Path to auth.json token file",
)
def commits(db_path, repos, all, auth):
    "Save commits for the specified repos"
    pass


@cli.command(name="scrape-dependents")
@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.argument("repos", type=str, nargs=-1)
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=True),
    default="auth.json",
    help="Path to auth.json token file",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Verbose output",
)
def scrape_dependents(db_path, repos, auth, verbose):
    "Scrape dependents for specified repos"
    pass


@cli.command()
@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=True),
    default="auth.json",
    help="Path to auth.json token file",
)
@click.option(
    "-f",
    "--fetch",
    is_flag=True,
    help="Fetch the image data into a BLOB column",
)
def emojis(db_path, auth, fetch):
    "Fetch GitHub supported emojis"
    pass


@cli.command()
@click.argument("url", type=str)
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=True),
    default="auth.json",
    help="Path to auth.json token file",
)
@click.option(
    "--paginate",
    is_flag=True,
    help="Paginate through all results",
)
@click.option(
    "--nl",
    is_flag=True,
    help="Output newline-delimited JSON",
)
@click.option(
    "--accept",
    help="Accept header to send, e.g. application/vnd.github.VERSION.html",
)
def get(url, auth, paginate, nl, accept):
    "Make an authenticated HTTP GET against the specified URL"
    pass


@cli.command()
@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.argument("repos", type=str, nargs=-1)
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=True),
    default="auth.json",
    help="Path to auth.json token file",
)
def workflows(db_path, repos, auth):
    "Fetch details of GitHub Actions workflows for the specified repositories"
    pass


