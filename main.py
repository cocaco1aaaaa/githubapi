from typing import Optional, List
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
import requests
import logging

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)  # Включаем логирование


class Repo(BaseModel):
    repo: str
    owner: str
    position_cur: int
    position_prev: int
    stars: int
    watchers: int
    forks: int
    open_issues: int
    language: str


class CommitActivity(BaseModel):
    date: str
    commits: int
    authors: List[str]


@app.get("/api/repos/top100")
async def get_top_repos(sort_by: Optional[str] = Query(None, description="Sort by field")):
    sort_options = ['repo', 'owner', 'position_cur', 'position_prev', 'stars', 'watchers', 'forks', 'open_issues',
                    'language']
    if sort_by is not None and sort_by not in sort_options:
        raise HTTPException(status_code=400,
                            detail="Invalid sort option.")  # Используем HTTPException для возврата ошибки клиенту

    params = {'q': 'stars:>1', 'sort': 'stars', 'order': 'desc', 'per_page': 100}
    if sort_by is not None:
        params['sort'] = sort_by

    try:
        response = requests.get('https://api.github.com/search/repositories', params=params)
        response.raise_for_status()  # Проверяем статус ответа
        data = response.json()['items']
    except Exception as e:
        logging.error(f"Error while fetching top repos: {e}")
        raise HTTPException(status_code=500, detail="Error while fetching top repos. Please try again later.") from e

    repos = []
    for idx, item in enumerate(data, start=1):
        repo = Repo(
            repo=item['full_name'],
            owner=item['owner']['login'],
            position_cur=idx,
            position_prev=0,  # You can calculate previous position if needed
            stars=item['stargazers_count'],
            watchers=item['watchers_count'],
            forks=item['forks_count'],
            open_issues=item['open_issues_count'],
            language=item['language']
        )
        repos.append(repo)

    return repos


@app.get("/api/repos/{owner}/{repo}/activity")
async def get_repo_activity(owner: str, repo: str, since: str, until: str):
    # You can implement this function to get commit activity for a specific repository within a time range
    pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

