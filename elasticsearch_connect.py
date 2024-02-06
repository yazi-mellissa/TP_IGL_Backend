from elasticsearch import Elasticsearch
from utils.Creds import ElasticsearchCreds

class ElasticsearchConnection:
    elasticsearch : Elasticsearch = None
    def __init__(self):
        self.elasticsearch = Elasticsearch(
            [{'host': ElasticsearchCreds.get("Host"), 'port': ElasticsearchCreds.get("Port"),'scheme':'https'}],
            http_auth=('elastic', ElasticsearchCreds.get("ApiKey")),
            verify_certs=False
        )
        try:
            if self.elasticsearch.ping():
                print("Connected to Elasticsearch")
            else:
                print("Unable to connect to Elasticsearch")
        except Exception as e:
            print(f"Error connecting to Elasticsearch: {str(e)}")

    def getEngine(self):
        return self.elasticsearch