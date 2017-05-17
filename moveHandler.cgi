#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, sqlite3
from database import DBHandler
from authentication import cookieAuthentication
from config import db_path
from os import environ
import postNugget
import mylog

def moveHandle(form, environ):
    result = cookieAuthentication(environ)

    if not result: return

    userid, username, usercookie = result

    topic_id = int(form.getvalue("topic_id"))
    docno = form.getvalue("docno")
    signal = form.getvalue("signal")

    atn_db  = DBHandler(db_path.atn)

    print("Content-Type: text/plain\r\n")

    if signal == 'm': #mark dont' have to switch doc
        atn_db.cur.execute('SELECT state FROM bookmark WHERE topic_id=? AND docno=?', [topic_id, docno])
        exist_check = atn_db.cur.fetchone()
        if not exist_check:
            atn_db.insert('bookmark',[None,topic_id,docno,1])
            print("0") #do nothing in the front-end
        else:
            state, = exist_check
            if state == 1: #already marked
                state += 1
                print("-1") #prompt unmark message
            else:
                print("0")
                state -= 1
            atn_db.cur.execute('UPDATE bookmark SET state=? WHERE topic_id=? AND docno=?',[state,topic_id,docno]) #toggle state between marked and unmarked
        atn_db.commit()
        atn_db.close()
        return


    # add the doc to filter_list as discarded doc
    if signal in ['r','d']:
        atn_db.cur.execute('SELECT * FROM filter_list WHERE topic_id=? AND docno=?', [topic_id, docno])
        exist_check = atn_db.cur.fetchone()
        if not exist_check:
            atn_db.insert('filter_list',[topic_id, docno, ['r','d'].index(signal)+2])
            atn_db.commit()
        else:
            print('-1')
            atn_db.close()
            return

        #atn_db.cur.execute('SELECT userid, topic_name, domain_id FROM topic WHERE topic_id=?',[topic_id])
        #userid, topic_name, domain_id= atn_db.cur.fetchone()
        
        #corpus = ['EBOLA', 'POLAR', 'WEAPON'][domain_id-1]
        cmd = ''
        if signal == 'd': cmd = 'DUPLICATE'
        if signal == 'r': cmd = 'IRRELAVANT'
        try: mylog.log_discard_doc(username, cmd.lower(), str(topic_id), docno)
        except: pass

    #table = 'search_list' 

    #if signal == 'p':
    #    atn_db.cur.execute('SELECT row_num, docno FROM %s WHERE topic_id=? AND row_num < (SELECT row_num FROM %s WHERE topic_id=? AND docno=?) ORDER BY row_num DESC LIMIT 1'%(table, table), [topic_id, topic_id, docno])
    #    try: mylog.log_prev_doc(username, str(topic_id), docno)
    #    except: pass
    #else:
    #if the op is discard or duplicate, go to the next doc by default
    #    atn_db.cur.execute('SELECT row_num, docno FROM %s WHERE topic_id=? AND row_num > (SELECT row_num FROM %s WHERE topic_id=? AND docno=?) LIMIT 1'%(table, table), [topic_id, topic_id, docno])
    #    if signal == 'n':
    #        try: mylog.log_next_doc(username, str(topic_id), docno)
    #        except: pass
    
    #tmpresult = atn_db.cur.fetchone()

    #if signal in ['d','r']:
    #    atn_db.cur.execute('DELETE FROM search_list WHERE topic_id=? AND docno=?',[topic_id, docno])
    #    atn_db.commit()

    #if tmpresult: 
    #    row_num, nextdoc = tmpresult
    #    print(nextdoc)
        # update topic last doc
    #    atn_db.cur.execute('UPDATE topic SET docno=? WHERE topic_id=?', [nextdoc, topic_id])
    #    atn_db.commit()
    #else: 
    #    print("0")
    table = 'search_list'
    tmpresult = None
    atn_db.cur.execute('SELECT round,row_num FROM %s WHERE topic_id=? AND docno=? ORDER BY round DESC LIMIT 1'%(table),[topic_id,docno])
    res = atn_db.cur.fetchone()
    if res:
        round,row_num = res
        if signal == 'p': #switch to the previous doc
            atn_db.cur.execute('SELECT docno FROM %s WHERE row_num=? AND round=?'%(table), [row_num-1,round])
            try: mylog.log_prev_doc(username, str(topic_id), docno)
            except: pass
        else: #switch to the next doc either by clicking next or marking the current doc irrelavant or duplicate
            atn_db.cur.execute('SELECT docno FROM %s WHERE row_num=? AND round=?'%(table), [row_num+1,round])
            try: mylog.log_next_doc(username, str(topic_id), docno)
            except: pass
        tmpresult = atn_db.cur.fetchone()

    if signal in ['d','r']:
        atn_db.cur.execute('DELETE FROM search_list WHERE topic_id=? AND docno=?',[topic_id, docno])
        atn_db.commit()

    if tmpresult:
        nextdoc, = tmpresult
        print(str(nextdoc))
        # update topic last doc
        atn_db.cur.execute('UPDATE topic SET docno=? WHERE topic_id=?', [nextdoc, topic_id])
        atn_db.commit()
    else:
        print("0")

    atn_db.close()

# __main__

form = cgi.FieldStorage()
moveHandle(form, environ)

