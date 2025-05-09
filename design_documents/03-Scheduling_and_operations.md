# Scheduling
The CI tooling already takes care of deploying changes to OpenSearch clusters. This time we need a scheduler.
This scheduler needs to schedule jobs at specific hours, have a log trail and have credentials management. Something like Jenkins will fit the bill.

# Operation Notes
- Official automation around the OpenSearch Alerting API does not seem to exist. The main effort would be to create something robust, beyond this proof-of-concept.
- Everything is Dockerized to maximize results reproducibility (anyone can run the tooling locally), ease of dependencies management and future proofing (lateral moves to other platforms like Openshift, Kubernetes, PaaS or simple Docker instances possible).
- With the approach we have taken, maintenance and evolution should be relatively simple. We can test our tooling against newer versions of OpenSearch easily (by changing the Docker test image), the user interface is well proven (here it is GitHub but it could be other similar solutions), dependencies can be updated easily and security can be ensured.
- Further constraints can be integrated into the validation/testing, for example to limit queries as to not overload the OpenSearch cluster.