#!/usr/bin/python
# -*- coding: utf-8 -*-
from authentication import cookieAuthentication
from os import environ
import cgi
from database import DBHandler










def moveHandle(form,environ):
    result = cookieAuthentication(environ)
    #a = open("result.txt","w")
    #a.write(str(result))
    #a.close()
    if not result: return
    userid, username, usercookie = result

    topic_id = int(form.getvalue("topic_id"))
    docno = form.getvalue("docno")
    signal = form.getvalue("signal")
    print("Content-Type: text/plain\r\n")
    atn_db = DBHandler(db_path.atn)
	else:
	    print("-1")
    except:
	print("-1")






form = cgi.FieldStorage()
moveHandle(form, environ)
