# Opensearch Monitors Repository
## Purpose
This repository is used to store your Opensearch monitors.
Define them in a single file, and we take care of the deployment.

## How can I add, modify and delete monitors
Please create a pull-request with your changes to the file `monitors.json`.
Once your changes are automatically checked and validated, you may merge your pull-request.

Opensearch Monitor changes are deployed every night at 01:00am GMT.
Check the deployment status at http://localhost:5000/

## Contact
Team X is responsible for this repository and deployment flows, contact team_a@company.local for support.

# For exercise evaluators
## How to run the solution locally
### Prerequisites
You need Docker (=>28.0.4) and Docker Compose (>=v2.34.0) installed.

### Launch
```
git clone https://github.com/khalid-zerouali/202505-work-exercise.git
cd 202505-work-exercise/
OPENSEARCH_INITIAL_ADMIN_PASSWORD="ThisIsAdiPass1*" OPENSEARCH_HOST=localhost docker compose -f docker-compose-opensearch-ci.yaml up opensearch-node1 opensearch-dashboards jenkins status_ui
```
- The Docker Compose command will build and launch the components automatically. Nothing else needs to be done.

### UI access
You may access the various UIs using the following addresses once everything is running:
- URL for OpenSearch: http://localhost:5601/app/login (login: admin/ThisIsAdiPass1*)
- URL for Jenkins: http://localhost:8080/
- URL for our status UI: http://localhost:5000/

### Cleanup/Rebuild
If you want to start from a clean state (configuration is saved when Docker containers are stopped):
```
cd 202505-work-exercise/
docker compose -f docker-compose-opensearch-ci.yaml down opensearch-node1 opensearch-dashboards jenkins status_ui -v

OPENSEARCH_INITIAL_ADMIN_PASSWORD="ThisIsAdiPass1*" OPENSEARCH_HOST=localhost docker compose -f docker-compose-opensearch-ci.yaml up opensearch-node1 opensearch-dashboards jenkins status_ui
```

## Design choices
The entrypoint will be [the design_documents/ folder](./design_documents), starting with the solution requirements file.
## Deliveries
For this exercise we have done a proof-of-concept and wrote associated documentation, explaining our assumptions and choices.
- Providing a way for users to submit their OpenSearch monitor changes.
- Automatically validating their input and changes.
- Testing these changes against an ephemeral OpenSearch instance.
- Deploying these changes periodically using a Jenkins instance and pipeline.
- Providing a deployment status UI for users.