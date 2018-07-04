# -*- coding: utf8 -*-
import json
import subprocess
import mysql.connector
from inputs_outputs import *
from django.db import IntegrityError

def getMaxheight():
    cnx = mysql.connector.connect(user='root', password='William2018!', host='localhost', database='blockchain')

    cursor = cnx.cursor()
    query_maxheight = ("SELECT MAX(height)" "FROM heighttxid")

    cursor.execute(query_maxheight)

    fetchedheight = cursor.fetchone()

    if fetchedheight[0] is None:
        maxheight=0
    else:
        maxheight=fetchedheight[0]

    cursor.close()
    cnx.close()

    return maxheight


cnx = mysql.connector.connect(user='root', password='William2018!', host='localhost', database='blockchain')

cursor = cnx.cursor()
add_heighttxid = ("INSERT IGNORE INTO heighttxid " "(height, txid) " "VALUES (%s, %s)")


maxheight = getMaxheight()
print(getNumberofblocks())


for i in range(maxheight+1, getNumberofblocks()):
    listoftransactionid = [] #reinitializing the list
    blockhash = getblockhashfromheight(i)
    block = getblockfromblockhash(blockhash)
    listoftransactionid = getlistoftransactionidfromblock(block)

    for j in range(0, len(listoftransactionid)):
        data_heighttxid = (i, listoftransactionid[j])

        try:
            # Insert new row
            cursor.execute(add_heighttxid, data_heighttxid)
        except IntegrityError as e:
            print("Duplicate on txid " + listoftransactionid[j])

cursor.close()
cnx.close()
