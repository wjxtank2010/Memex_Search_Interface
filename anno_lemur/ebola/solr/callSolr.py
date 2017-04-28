import sys
sys.path.insert(0,"/data2/apps/anaconda2/lib/python2.7/site-packages")
import certifi
import requests,os,yaml,sys,re,json
from requests.auth import HTTPBasicAuth
from elasticsearch import Elasticsearch

#solrURL = "http://cs-sys-1.uis.georgetown.edu/solr/ebola/browse?wt=json&start=0&rows=600&q=%s"%sys.argv[1]
#username = "infosense"
#password = "test@123"
query = sys.argv[1]
query = re.sub("%3A",":",query)
query = re.sub("%3B",";",query)
query_terms = query[:-1].split(";")
query_pair = map(lambda x:x.split(":"),query_terms)
query_string = " ".join(map(lambda x:x[1],query_pair))
f = open("a.txt","w")
f.write(query_string)
f.close()
query_body = {"size":500,"query":{"bool":{"must":{"match":{"raw_content": query_string}}}}}
es = Elasticsearch(["localhost:9200/gt"],request_timeout=60)
response = es.search(body=query_body,request_timeout=60)
documents = response["hits"]["hits"]
for document in documents:
    print document["_id"]

#r = requests.get(solrURL, auth=HTTPBasicAuth(username, password))

#data = json.loads(r.content)

#for doc in data['response']['docs']:
   # print doc['id']
