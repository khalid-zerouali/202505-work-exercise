# Business Requirements
We have been asked to implement an automated solution that can deploy OpenSearch monitors with minimum effort.
https://docs.opensearch.org/docs/latest/observing-your-data/alerting/monitors/

Submissions are to be deployed every night.
The suggestion was to define these monitors in JSON format, ultimately these entries are deployed on real OpenSearch instances, see screenshot for the expected result:
![result](screenshots/os_dashboard.png?raw=true)

## Entrypoint for the business user
In the scope of this exercise we have made use of the GitHub ecosystem to automate this change flow. However we can substitute every part of this modular solution with what is available at the company.
This concretely means:
1. Our user needs to connect to the SCM (GitHub), make their change (user should be able to make simple changes through git).
2. They are at this point authenticated, their changes are tracked and verified. They will only be able to merge their changes once the automated tests are successful.
3. Our automation deploys the changes at night, user can follow the deployment status. Hopefully they are happy with the result.
4. In case of support needs, the user can make use of ticket style support through the SCM or directly through their pull-requests.