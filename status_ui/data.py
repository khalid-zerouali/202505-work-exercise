dummy_monitor_json = {
               "type": "monitor",
               "name": "dummy_monitor",
               "monitor_type": "query_level_monitor",
               "enabled": "false",
               "schedule": {
                 "period": {
                   "interval": 10,
                   "unit": "MINUTES"
                 }
               },
               "inputs": [{
                 "search": {
                   "indices": [".plugins-ml-config"],
                   "query": {
                     "query": {
                         "match": {
                             "message": "dummy message"
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