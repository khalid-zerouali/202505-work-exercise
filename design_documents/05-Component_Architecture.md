# Component Architecture
This solution is composed of various components:
- An agentless Jenkins instance (defined in `Dockerfile.scheduler` and `docker-compose-opensearch-ci.yaml`).
- A single node OpenSearch instance (defined in `docker-compose-opensearch-ci.yaml`) that hosts data, indexes and monitors.
- A OpenSearch Dashboards instance (defined in `docker-compose-opensearch-ci.yaml`) that users can connect to to explore data.
- A web server, Flask (defined in `Dockerfile.status-ui` and `docker-compose-opensearch-ci.yaml`) that serves the Status UI.
These components are deployed with Docker/Docker Compose and are hosted on the same network.
- Finally, a schema validator (defined in `Dockerfile.validator` and `docker-compose-validator.yaml`). This is used in GitHub Action to validate the JSON file against the data schema.

## Folders
- `monitors_validator/` contains the data schema definition (monitors_schema-v1.0.0.json) and its HTML version that users can check.
- `opensearch_ci/` contains scripts needed to create and manage OpenSearch indices and monitors, this is used by the Jenkins pipeline and GitHub Actions.
- `scheduler_config/` contains Jenkins configuration and pipeline automation files (Groovy), everything is pre-configured when Jenkins starts up for the first time.
- `status_ui/` contains the Flask web application. This applications retrieves data (JSON file, API data from Jenkins and OpenSearch endpoints).
- `.github/workflows` contains the GitHub Actions workflow. It triggers jobs on GitHub following pull-request actions (opening, reopening) and runs automation processes on their own nodes. It makes use of their credential management services (through the injection of environment variables stored as secrets).