# March 6 change display first pre-annotation result to display search feature if in pre-annotation
# author: Sharon
import sys
import re
sys.path.append("../../../")
from database import DBHandler

def extractFeature(inputString, dic):
    # get name to display for snippet
    nameTagContent = inputString[inputString.index("<name>"):inputString.index("</name>")]
    name_to_display = ""
    if nameTagContent:
        names = nameTagContent.split(",")
        if "name" in dic and dic["name"] and dic["name"].lower() in nameTagContent.lower():
            name_to_display = dic["name"].capitalize()
        else:
            name_to_display = names[0].lstrip("<name>name: ").capitalize()

    # age
    ageTagContent = inputString[inputString.index("<age>"):inputString.index("</age>")]
    age_to_display = ""
    if ageTagContent:
        ages = ageTagContent.lstrip("<age>age:").split(",")
        if "age" in dic and dic["age"]:
            minAge = dic["age"][:2]
            maxAge = dic["age"][2:]
            # age_found = False
            for age in ages:
                if int(age) >= int(minAge) and int(age) <= int(maxAge):
                    # age_found = True
                    age_to_display = age
                    break
            # if age_found:
            #     age_to_display = minAge + " to " + maxAge
        if not age_to_display:
            age_to_display = ages[0]

    # phone
    phoneTagContent = inputString[inputString.index("<phone>"):inputString.index("</phone>")]
    phone_to_display = ""
    if phoneTagContent:
        phones = phoneTagContent.split(",")
        if "phone" in dic and dic["phone"] and dic["phone"] in phones:
            phone_to_display = dic["phone"]
        else:
            phone_to_display = phones[0].lstrip("<phone>phone:")

    # ethnicity / nationality
    #a = open("ethnicity.txt","a")
    ethnicityTagContent = inputString[inputString.index("<ethnicity>"):inputString.index("</ethnicity>")]
    ethnicity_to_display = ""
    #a.write("tagContent: "+ethnicityTagContent+"\n")
    if ethnicityTagContent:
        nationalities = ethnicityTagContent.split(",")
        #a.write("nationalities: "+str(nationalities)+"\n")
        if "nationality" in dic and dic["nationality"] and dic["nationality"].lower() in ethnicityTagContent.lower():
            ethnicity_to_display = dic["nationality"]
        else:
            ethnicity_to_display = nationalities[0].lstrip("<ethnicity>ethnicity: ").capitalize()
        #a.write("ethnicity_to_display: "+ethnicity_to_display+"\n")
    # location
    locationTagContent = inputString[inputString.index("<location>"):inputString.index("</location>")]
    location_to_display = ""
    if locationTagContent:
        locations = locationTagContent.split(",")
        if "state" in dic and dic["state"] and dic["state"].lower() in locationTagContent.lower():
            location_to_display = dic["state"]
            if "city" in dic and dic["city"] and dic["city"] in locationTagContent:
                location_to_display = dic["city"] + ", " + location_to_display
        else:
            location_to_display = locations[0].lstrip("<location>location:")

    # hair_color
    hairColorTagContent = inputString[inputString.index("<hair_color>"):inputString.index("</hair_color>")]
    hairColor_to_display = ""
    if hairColorTagContent:
        hairs = hairColorTagContent.split(",")
        if "hairColor" in dic and dic["hairColor"] and dic["hairColor"].lower() in hairColorTagContent.lower():
            hairColor_to_display = dic["hairColor"]
        else:
            hairColor_to_display = hairs[0].lstrip("<hair_color>hair_color:")

    result = [name_to_display,age_to_display,phone_to_display,ethnicity_to_display,location_to_display,hairColor_to_display]
    delimeter = "SharonDelimeter"
    print(delimeter.join(result)+delimeter)

def extractImg(inputString):
    imgTagPattern = r"<img.*?>"
    results = re.findall(imgTagPattern,inputString)
    imgResult = []
    for result in results:
        urlPattern = r"src=[\'\"](.*?)[\'\"]"
        src = re.findall(urlPattern,result)
        if src:
            imgResult.append(src[0])
    imgResult = imgResult[:3] #only show the first 3 images
    delimeter = "ImageDelimeter"
    if imgResult:
        print(delimeter.join(imgResult)+delimeter)

def getQuery(atn_db,topicId):
    atn_db.cur.execute("SELECT para from topic where topic_id=?",[topicId])
    para, = atn_db.cur.fetchone()
    paraParts = para.split("&",3)
    queryFieldCount = int(paraParts[2].lstrip("N="))
    query = paraParts[3][:-1]#delete the last ;
    query_terms = query.lstrip("q=").split(";",queryFieldCount-1)
    query_dic = {x.split(":",1)[0]:x.split(":",1)[1] for x in query_terms}
    return query_dic

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")
    atn_db  = DBHandler("../../../database/Memex.db") #database connection
    topicId = int(sys.argv[1]) #topic id

    f = open(str(topicId)+".txt") # read document content
    lines = f.readlines()
    f.close()
    query_dic = getQuery(atn_db,topicId)
    inputString = " ".join(lines)
    extractFeature(inputString, query_dic)  # match query key word with doc pre-annotation
    extractImg(inputString)
