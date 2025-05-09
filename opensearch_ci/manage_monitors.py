import json
import re
import logging
from opensearchpy import OpenSearch

log = logging.getLogger('app')
log.setLevel(logging.INFO)

# Logging
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


#TODO: json file already validated by the schema validator upstream
#      but it never hurts to check twice
#NOTE: .opendistro-alerting-config index is not created until
#      the first monitor is created.
def update_monitors_on_opensearch(os_client, monitors_json_path):
    with open(monitors_json_path) as monitors_json_file:
        monitors_json = json.load(monitors_json_file)
        for monitor in monitors_json['Monitors']:
            log.info(monitor)
            body = create_monitor_json(monitor)
            response = os_client.plugins.alerting.create_monitor(body)
            #print(response)
            query = create_search_query_monitor(monitor['Monitor_Name'])
            response = os_client.plugins.alerting.search_monitor(query)
            #print(response)


def create_search_query_monitor(name):
    query = {
      "query": {
        "match" : {
          "monitor.name": name
        }
      }
    }
    return query


def create_monitor_json(monitor):
    # Turn user input for intervals into something usable by OpenSearch
    p = re.compile('(\d+)\s*(\w+)')
    interval_number, unit_input = p.match(monitor['Time2Scan']).groups()
    unit = ''
    if unit_input == 'm':
        unit = 'MINUTES'
    else:
        raise TypeError("Monitor interval unit is not recognized")

    json = {
               "type": "monitor",
               "name": monitor['Monitor_Name'],
               "monitor_type": "query_level_monitor",
               "enabled": monitor['is_active'],
               "schedule": {
                 "period": {
                   "interval": interval_number,
                   "unit": unit
                 }
               },
               "inputs": [{
                 "search": {
                   "indices": [monitor['Index']],
                   "query": {
                     "query": {
                         "match": {
                             "message": monitor['Text2Scan_in_Message']
                         }
                     }
                   }
                 }
               }],
               "triggers": [{
                 "name": "test-trigger",
                 "severity": "1",
                 "condition": {
                   "script": {
                     "source": "ctx.results[0].hits.total.value > 0",
                     "lang": "painless"
                   }
                 },
                 "actions": [{
                   "name": "test-action",
                   "destination_id": "tobedefined",
                   "message_template": {
                     "source": "This is my message body."
                   },
                   "throttle_enabled": True,
                   "throttle": {
                     "value": 10,
                     "unit": "MINUTES"
                   },
                   "subject_template": {
                     "source": "The Subject"
                   }
                 }]
               }]
            }
    return json