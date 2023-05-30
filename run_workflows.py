import yaml
from github import Github

# Load configuration from config.yaml
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

# Set up your GitHub access token
ACCESS_TOKEN = config["github_token"]
ORGANIZATION = config["organization"]

# Define the organization and workflow file name
WORKFLOW_FILE = ".github/workflows/sonarqube.yml"


# Helper function to trigger workflow
def trigger_workflow(repository, workflow_id):
    repository.get_workflow(workflow_id).rerun()
    print(f"Triggered workflow for repository '{repository.full_name}'")


# Initialize the GitHub API client
g = Github(ACCESS_TOKEN)

# Get the organization
org = g.get_organization(ORGANIZATION)

# Get a list of all repositories in the organization
repositories = org.get_repos()

# Iterate over repositories
for repository in repositories:
    print(repository.name)
    # Check if 'sonarqube.yml' workflow exists
    workflows = repository.get_workflows()
    sonarqube_workflow = next((wf for wf in workflows if wf.path == WORKFLOW_FILE), None)

    if sonarqube_workflow:
        # Check if the last run failed
        runs = sonarqube_workflow.get_runs()
        last_run = next(iter(runs))
        if last_run.conclusion == "failure":
            # Trigger the workflow again
            last_run.rerun()
            print(f"Triggered workflow for repository '{repository.full_name}'")
