import requests
import confidence

def get_all_pull_requests(repo_owner, repo_name, token):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        pull_requests = response.json()
        return pull_requests
    else:
        print(f"Failed to fetch pull requests. Status code: {response.status_code}")
        return []

# Пример использования
repo_owner = confidence.repo_owner  # Имя владельца репозитория
repo_name = confidence.repo_name  # Название репозитория
access_token = confidence.access_token  # Ваш токен доступа

pull_requests = get_all_pull_requests(repo_owner, repo_name, access_token)
for index, pr in enumerate(pull_requests, start=1):
    pr_number = pr['number']
    pr_title = pr['title']
    pr_url = pr['html_url']
    pr_author = pr['user']['login']

    print(f"{index} Pull Request #{pr_number}: {pr_title}")
    print(f"URL: {pr_url}")
    print(f"Author: {pr_author}")
    print()