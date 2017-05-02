import sys
sys.path.insert(0,"/data2/apps/anaconda2/lib/python2.7/site-packages")
sys.path.append("../../../")
from database import DBHandler
import certifi,os,yaml,re,json,urllib
from fuzzywuzzy import fuzz
from elasticsearch import Elasticsearch,RequestsHttpConnection


def getQuery(atn_db,topicId):
	atn_db.cur.execute("SELECT para from topic where topic_id=?",[topicId])
	para, = atn_db.cur.fetchone()
	paraParts = para.split("&",3)
	queryFieldCount = int(paraParts[2].lstrip("N="))
	query = paraParts[3][:-1]#delete the last ;
	query_terms = query.lstrip("q=").split(";",queryFieldCount-1)
	query_dic = {x.split(":",1)[0]:x.split(":",1)[1] for x in query_terms}
	return query_dic

def main():
	atn_db  = DBHandler("../../../database/Memex.db") #database connection
	topicId = int(sys.argv[1]) #topic id
	must_list = []
	should_list = []
	query_dic = getQuery(atn_db,topicId)
	age_min = 0
	age_max = 0
	height_min = 0
	height_max = 0
	query_body = {"size":500,"query":{"bool":{"must":[],"should":[]}} }
	feature_should_search_map = {"name":"name","hairColor":"hair","eyeColor":"eye","nationality":"nationality","ethnicity":"ethnicity","reviewSite":"review","reviewSiteId":"review","email":"email","phone":"phone","state":"","city":"","price":"","multiple_providers":"","socialMedia":"","socialMediaId":"","services":"","height":"height","weight":"weight","post_date":"posted"}
	for key in query_dic:
		if key in ["phone","age","height","hairColor","eyeColor"]: #field search
			pass
		else:
			must_list.append(query_dic[key])
	if "age" in query_dic:
		age_min = int(query_dic["age"][:2])
		age_max = int(query_dic["age"][2:])
		should_list.append("age")
	if "height" in query_dic:
		height_min = int(query_dic["height"][:3])
		height_max = int(query_dic["height"][3:])
		should_list.append("height")
	if must_list: #plain text search fields
		query_body["query"]["bool"]["must"].append({"match":{"raw_content":" ".join(must_list)}})
	else: #field search
		query_list = []
		if "age" in query_dic:
			query_list.append("age")
		if "height" in query_dic:
			query_list.append("height")
		query_body["query"]["bool"]["must"].append({"match":{"raw_content":" ".join(query_list)}})
	#should_arr = []
	# for word in should_list:
	# 	dic = {}
	# 	dic["match"] = {}
	# 	dic["match"]["raw_content"] = word
	# 	should_arr.append(dic)
	#query_body["query"]["bool"]["should"] = should_arr
	if "phone" in query_dic:
		phone_number = re.sub("\D","",query_dic["phone"])
		query_body["query"]["bool"]["must"].append({"match":{"phone":phone_number }})
	if "age" in query_dic:
		query_body["query"]["bool"]["must"].append({"range" : {"age" : {"gte" : age_min,"lte" : age_max}}})
	if "height" in query_dic:
		query_body["query"]["bool"]["must"].append({"range" : {"height" : {"gte" : height_min,"lte" : height_max}}})
	if "hairColor" in query_dic:
		query_body["query"]["bool"]["must"].append({"match":{"hairColor":" ".join(query_dic["hairColor"].split(","))}})
	if "eyeColor" in query_dic:
		query_body["query"]["bool"]["must"].append({"match":{"eyeColor":" ".join(query_dic["eyeColor"].split(","))}})
	raw_content_str = query_body["query"]["bool"]["must"][0]
	if not raw_content_str["match"]["raw_content"]: #occurs when field search(phone,hairColor,eyeColor) is the only field involved
		query_body["query"]["bool"]["must"].pop(0)
	a = open("test.txt","w")
	a.write(str(query_body))
	a.close()
	es = Elasticsearch(["localhost:9200/positiongt"],request_timeout=60)
	response = es.search(body=query_body,request_timeout=60)
	documents = response["hits"]["hits"]
	results = []
	if not documents:
		hypoFields = []
		if "hairColor" in query_dic:
			hypoFields.append("hairColor")
		if "eyeColor" in query_dic:
			hypoFields.append("eyeColor")
		is_raw_content = False
		if hypoFields: #if there is no results and hairColor or eyeColor included, transfer field search(originally hairColro and eyeColor are field search) to plain text search
			for term in hypoFields:
				j = -1
				for i in range(len(query_body["query"]["bool"]["must"])):
					if "raw_content" in query_body["query"]["bool"]["must"][i]["match"]:
						query_body["query"]["bool"]["must"][i]["match"]["raw_content"] += " "+" ".join(query_dic[term].split(","))
						is_raw_content = True
					if term in query_body["query"]["bool"]["must"][i]["match"]:
						j = i
				if j>=0:
					query_body["query"]["bool"]["must"].pop(j) #remove the field search
			if not is_raw_content: #this case occurs when field search are the only fields involved.
				query_body["query"]["bool"]["must"].insert(0,{"match":{"raw_content":" ".join(map(lambda x:" ".join(query_dic[x].split(",")),hypoFields))}})
			response = es.search(body=query_body,request_timeout=60)
			documents = response["hits"]["hits"]
	if "ethnicity" in query_dic:
		f = open("nation_continent.txt")
		ethnicity_dic = yaml.load(f)
		candidate_countries = ethnicity_dic[query_dic["ethnicity"].lower()]+[query_dic["ethnicity"].capitalize()]
		for document in documents:
			if "ethnicity" in document["_source"] and document["_source"]["ethnicity"]:
				ethnicities = map(lambda x:x.lower(),document["_source"]["ethnicity"])
				#print(ethnicities)
				if query_dic["ethnicity"].capitalize() in ethnicities:
					print(document["_id"])
					results.append(document["_id"])
				else:
					isMatch = False
					for eth_candi in ethnicities:
						if isMatch:
							break
						for coun_candi in candidate_countries:
							if fuzz.ratio(eth_candi,coun_candi.lower())>=80:
								print(document["_id"])
								results.append(document["_id"])
								isMatch = True
								break

	else:
		for document in documents:
			print document["_id"]
			results.append(document["_id"])
	atn_db.cur.execute("SELECT round from search_list where topic_id=? ORDER BY round DESC LIMIT 1",[topicId])
	res = atn_db.cur.fetchone()
	round = 0
	if res:
		round, = res
	round += 1
	for documentId in results:
		#print((None,topicId,round,documentId))
		atn_db.cur.execute('INSERT INTO %s VALUES(%s)' %("search_list", "?,?,?,?"), (None,topicId,round,documentId))
	atn_db.commit()
	atn_db.close()

if __name__ == "__main__":
	main()


