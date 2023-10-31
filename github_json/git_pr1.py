import requests

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

def get_reviewers(pull_request_reviews_url, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(pull_request_reviews_url, headers=headers)

    if response.status_code == 200:
        reviews = response.json()
        reviewers = [review['user']['login'] for review in reviews]
        return reviewers
    else:
        print(f"Failed to fetch reviewers for Pull Request. Status code: {response.status_code}")
        return []

# Пример использования
repo_owner = "tel-ran-de"  # Имя владельца репозитория
repo_name = "codility-tasks"  # Название репозитория
access_token = "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"  # Ваш токен доступа

pull_requests = get_all_pull_requests(repo_owner, repo_name, access_token)
for index, pr in enumerate(pull_requests, start=1):
    pr_number = pr['number']
    pr_title = pr['title']
    pr_url = pr['html_url']
    pr_author = pr['user']['login']
    pr_reviews_url = pr['url'] + "/reviews"

    print(f"{index} Pull Request #{pr_number}: {pr_title}")
    print(f"URL: {pr_url}")
    print(f"Author: {pr_author}")

    reviewers = get_reviewers(pr_reviews_url, access_token)
    if reviewers:
        print(f"Reviewers: {', '.join(reviewers)}")

    print()
