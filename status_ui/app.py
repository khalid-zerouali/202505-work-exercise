import requests, json, logging, os
from flask import Flask, render_template
from opensearchpy import OpenSearch
from data import dummy_monitor_json
from datetime import datetime


app = Flask(__name__)
GITHUB_JSON_URL = "https://raw.githubusercontent.com/khalid-zerouali/202505-work-exercise/refs/heads/main/monitors.json"
JENKINS_JSON_URL = "http://jenkins:8080/job/opensearch-monitors-deployment-pipeline/wfapi/runs"

# Logging
log = logging.getLogger('status_ui')
log.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


# Fetch the committed JSON file containing monitors definition
def retrieve_remote_json(url):
    response = requests.get(url)
    return response.text


def create_search_query_monitor(name):
    query = {
      "query": {
        "match" : {
          "monitor.name": name
        }
      }
    }
    return query


def is_monitor_deployed(monitor_name, os_client):
    query = create_search_query_monitor(monitor_name)
    response = os_client.plugins.alerting.search_monitor(query)
    
    log.debug("Monitor: " + monitor_name + ", API response: " + str(response))
    if response["hits"]["total"]["value"] > 0:
        return True
    else:
        return False


# For each monitor, add its deployment status
def add_deployment_status(monitors_dict):
    # Create OpenSearch client
    host = os.environ['OPENSEARCH_HOST']
    port = 9200
    auth = ('admin', os.environ['OPENSEARCH_INITIAL_ADMIN_PASSWORD'])

    os_client = OpenSearch(
        hosts = [{'host': host, 'port': port}],
        http_auth = auth,
        use_ssl = True,
        verify_certs = False
    )

    # Workaround bug https://forum.opensearch.org/t/opendistro-alerting-config-not-created/16667
    response = os_client.plugins.alerting.create_monitor(dummy_monitor_json)
    log.debug("Workaround API: " + str(response))

    # Add deployment status
    for monitor in monitors_dict['Monitors']:
        monitor['status'] = is_monitor_deployed(monitor['Monitor_Name'], os_client)
        log.info("Monitor: " + monitor['Monitor_Name'] + ", Status: " + str(monitor['status']))

    return monitors_dict


def format_timestamp(pipelines):
    for pipeline in pipelines:
        pipeline['startTimeMillis'] = str(datetime.fromtimestamp(pipeline['startTimeMillis'] /1000.0))
        pipeline['endTimeMillis'] = str(datetime.fromtimestamp(pipeline['endTimeMillis'] /1000.0))
    return pipelines


@app.route('/')
def show_status():
    monitors_json_content = retrieve_remote_json(GITHUB_JSON_URL)
    monitors = json.loads(monitors_json_content)
    log.info("JSON retrieved from GitHub: " + str(monitors))
    monitors = add_deployment_status(monitors)

    pipeline_json_content = retrieve_remote_json(JENKINS_JSON_URL)
    log.info("Pipeline JSON retrieved from Jenkins: " + str(pipeline_json_content))
    pipelines = format_timestamp(json.loads(pipeline_json_content))

    return render_template('index.html', monitors=monitors['Monitors'], pipeline_runs=pipelines)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)