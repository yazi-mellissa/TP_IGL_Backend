from elasticsearch import Elasticsearch

def get_elasticsearch():
    return  Elasticsearch(    
    [{'host': 'localhost', 'port': 9200,'scheme':'https'}],  
    http_auth=('elastic', 'LNZ*SL+ZG110BGaw3N8f'),  verify_certs=False
)