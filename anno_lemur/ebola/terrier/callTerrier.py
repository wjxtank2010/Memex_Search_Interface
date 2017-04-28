import requests
import sys
import re

terrierURL = "http://localhost:9998/results.jsp?query=%s"%sys.argv[1].replace('.','')

r = requests.get(terrierURL)

results = re.findall('<span class=\"results_docno\">(.*?)</span>', r.content)

for result in results:
    print result

