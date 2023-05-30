import requests
import yaml


def get_queued_workflow_count(owner, repo, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    params = {
        "status": "queued"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        queued_workflows_count = len(data["workflow_runs"])
        return queued_workflows_count
    else:
        print(f"Failed to retrieve queued workflows. Status code: {response.status_code}")
        return None


def get_queued_workflow_count_for_org(org_name, token):
    url = f"https://api.github.com/orgs/{org_name}/repos"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    params = {
        "type": "all",
        "per_page": 100
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        queued_workflows_count = 0
        for repo in data:
            owner = repo["owner"]["login"]
            repo_name = repo["name"]
            repo_count = get_queued_workflow_count(owner, repo_name, token)
            if repo_count is not None:
                print(repo_name + str(repo_count))
                queued_workflows_count += repo_count
        return queued_workflows_count
    else:
        print(f"Failed to retrieve organization repositories. Status code: {response.status_code}")
        return None


# Read configuration from config.yaml file
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# Retrieve GitHub configuration values
token = config['github_token']
organization = config['organization']

queued_count = get_queued_workflow_count_for_org(organization, token)
if queued_count is not None:
    print(f"Number of queued workflows in the organization: {queued_count}")
