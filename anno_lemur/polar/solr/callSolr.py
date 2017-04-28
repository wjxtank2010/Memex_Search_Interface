import requests
from requests.auth import HTTPBasicAuth
import sys
import json

solrURL = "http://cs-sys-1.uis.georgetown.edu/solr/polar/browse?wt=json&start=0&rows=600&q=%s"%sys.argv[1]
username = "infosense"
password = "test@123"

r = requests.get(solrURL, auth=HTTPBasicAuth(username, password))

data = json.loads(r.content)

for doc in data['response']['docs']:
    print doc['id']
