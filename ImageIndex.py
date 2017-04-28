__author__ = 'infosense'
from imageDatabase import DBHandler
import re,sys,json
from bs4 import BeautifulSoup

def main():
    reload(sys)
    sys.setdefaultencoding("utf-8")
    index_path = "/data2/home/jw1498/GT_text_doc/GT_6.json"
    output_path = "GT_Cached_Doc/GT_6.json"
    db = DBHandler("MemexImage.db")
    with open(index_path) as f:
        with open(output_path,"w") as o:
            for line in f:
                doc = json.loads(line)
		doc_id = doc["_id"]
                try:
                    parent_url = doc["url"]      # doc original url
                    #print(parent_url)
                    if doc["raw_content"]:
                        text = doc["raw_content"]
                        soup = BeautifulSoup(text, "html.parser")
                        img_tags = soup.find_all("img")
                        # print(len(img_tags))
                        unique_img_tags = list(set(img_tags))
                        #print len(unique_img_tags)
                        for img in unique_img_tags:
                            img_url = img.get("src")    # Get img url from html
                            db.cur.execute("SELECT imgPath from MemexImgTable where origURL=?",[img_url])
                            result = db.cur.fetchone()
                            if result:
                                img_path, = result
                                img_path = img_path.replace("/data2/home/jw1498","http://cs-sys-1.uis.georgetown.edu/~jw1498")
                                text = text.replace(img_url,img_path)
                        doc["raw_content"] = text
                    json.dump(doc,o)
                    o.write("\n")
                except:
		    json.dump(doc,o)
		    o.write("\n")
                    #with open("errorlog","a") as e:
                    #    e.write(doc_id)
                    #    e.write("\n")
                    #    e.close()
		    
main()
