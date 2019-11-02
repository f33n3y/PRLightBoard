from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v5_1.git.models import GitPullRequestSearchCriteria

# Setup connection to AzureDevOps
personal_access_token = 'xxx'
organization_url = 'https://dev.azure.com/xxx'
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# Get projects
projects_list = []
core_client = connection.clients.get_core_client()
get_projects_response = core_client.get_projects()
index = 0
while get_projects_response is not None:
    for project in get_projects_response.value:
        projects_list.append(project)
        index += 1
    if get_projects_response.continuation_token is not None and get_projects_response.continuation_token != "":
        # Get the next page of projects
        get_projects_response = core_client.get_projects(continuation_token=get_projects_response.continuation_token)
    else:
        # All projects have been retrieved
        get_projects_response = None

total_prs_count = 0
git_client = connection.clients.get_git_client()
search_criteria = GitPullRequestSearchCriteria()

for project in projects_list:
    projects_pull_requests = git_client.get_pull_requests_by_project(project.id, search_criteria)
    print("PRs for " + project.name + " = " + str(len(projects_pull_requests)))
    total_prs_count += len(projects_pull_requests)

print("Total PRs: " + str(total_prs_count))
