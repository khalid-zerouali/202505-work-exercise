# Input Validation
We offer to the user a description of how the JSON file should look like and what are the constraints on it. They have access to an HTML page (or the equivalent data schema in JSON format):
![schema html](screenshots/schema_html.png?raw=true "HTML version of JSON data schema.")

This schema enforces all syntaxical and other constraints. Meaning it will be able to catch most common data entry mistakes.

# Continuous Integration
Our user creates their pull-request, from this interface they will be able to see the validation status and eventually ping us in case of difficult issues (they have access to logs directly from the SCM also):
![pr](screenshots/pull_request.png?raw=true)

## CI Workflow
For this proof-of-concept we have two tests. One verifies that the data is valid, the second that the changes can be deployed on OpenSearch through the Alerting API with the automation:
![workflow](screenshots/github_actions_workflow.png?raw=true)