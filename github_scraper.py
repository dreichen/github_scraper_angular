import requests
from tabulate import tabulate
import time

SLEEP_TIME = 90

with open("github-token.txt", "r") as token_file:
    TOKEN = token_file.read().strip("\n")

def search_github(url, query):
    params = {
        "q": query
    }
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"token {TOKEN}"
    }
    req = requests.get(url, params=params, headers=headers)
    return req.json() if req.status_code == 200 else {"total_count": req.json()["message"]}

def get_count(endpoint, query):
    return search_github(f"https://api.github.com/search/{endpoint}", query)["total_count"]

def build_table(settings):
    result = []
    for name, query, endpoint in settings:
        result.append([name, get_count(endpoint, query)])
        time.sleep(SLEEP_TIME)

    return tabulate(result, headers=["Type", "#"], tablefmt="latex")

table = build_table([
    # name in table                         # github search query                                   # endpoint, e.g. code, repositories, commits (see https://docs.github.com/en/rest/search#about-the-search-api for different endpoints)
    ("Angular Repository Count",            "angular+language:angular",                             "repositories"),
    ("Total Components Count",              "filename:*.component.ts+language:angular",             "code"),
    ("Total Component Tests Count",         "filename:*.component.spec.ts+language:angular",        "code"),
    ("Total Services Count",                "filename:*.service.ts+language:angular",               "code"),
    ("Total Service Tests Count",           "filename:*.service.spec.ts+language:angular",          "code"),
    # ("Total Directives Count",              "filename:*.directive.ts+language:angular",             "code"),
    # ("Tests with at least 3 tests",         "describe>=3 filename:*.spec.ts+language:angular",      "code"),
])

print(table)