import os
from pathlib import Path
from opensearchpy import OpenSearch
from data import *
from manage_monitors import update_monitors_on_opensearch


# Create OpenSearch index on a remote instance
def create_os_index(os_client, index_name):
    index_body = {
      'settings': {
        'index': {
          'number_of_shards': 2
        }
      },
      'mappings': {
        'properties': {
          'origin': {
            'type': 'text'
          },
          'message': {
            'type': 'text'
          },
          'created_date': {
            'type': 'date',
            'format' : 'MM/dd/yyyy'
          },          
        }
      },
    }
    response = os_client.indices.create(
      index_name, 
      body=index_body
    )
    return response


if __name__ == "__main__":
    root_dir = Path(__file__).resolve().parent.parent
    # Create OpenSearch client
    host = os.environ['OPENSEARCH_HOST']
    port = 9200
    auth = ('admin', os.environ['OPENSEARCH_INITIAL_ADMIN_PASSWORD'])

    client = OpenSearch(
        hosts = [{'host': host, 'port': port}],
        http_auth = auth,
        use_ssl = True,
        verify_certs = False
    )
    #info = client.info()
    #print(f"Welcome to {info['version']['distribution']} {info['version']['number']}")

    # Create our three indexes
    for index_name in ['index_a', 'index_b', 'index_c']:
        if not client.indices.exists(index_name):
            res_a = create_os_index(client, index_name)
            print(res_a)

    # Add documents to one index
    for doc in [document_a, document_b, document_c]:
        response = client.index(index = 'index_a',
                                body = doc,
                                refresh = True)

    # Update monitors
    monitors_json_file = root_dir / "monitors.json"
    update_monitors_on_opensearch(client, monitors_json_file)