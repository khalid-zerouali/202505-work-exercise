## Local run

We start locally an empty instance of OpenSearch, its UI and a Jenkins instance.
URL for OpenSearch: http://localhost:5601/app/login (login: admin/ThisIsAdiPass1*)
URL for Jenkins: http://localhost:8080/
URL for our status UI: http://localhost:5000/
```
OPENSEARCH_INITIAL_ADMIN_PASSWORD="ThisIsAdiPass1*" OPENSEARCH_HOST=localhost docker compose -f docker-compose-opensearch-ci.yaml up opensearch-node1 opensearch-dashboards jenkins status_ui
```