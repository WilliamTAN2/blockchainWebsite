# -*- coding: utf8 -*-
import os
from time import *
import subprocess
import re
import json
from collections import Counter
import mysql.connector
import heapq

BITCOIND_PATH = '/home/abrochec/blockchain/bitcoin-0.16.1'

cnx = mysql.connector.connect(user='root', password='Alexis2018!',host='localhost',database='miners', buffered=True) #10
cursor = cnx.cursor(buffered=True)


def get_children(transactionid, delai):
        timestamp = get_timestamp(transactionid) + int(delai)
        children=[]
        elements=[]
        query=("SELECT transaction FROM transactions WHERE previoustransaction LIKE  '%"+transactionid+"%' and timestamp<"+str(timestamp))
        cursor.execute(query)
        elements=cursor.fetchall()
        for i in elements:
                children.append(''.join(i))
        return(children)


def get_timestamp(transactionid):
        timestamp=[]
        query=("SELECT timestamp FROM transactions WHERE transaction LIKE  '"+transactionid+"'")
        cursor.execute(query)
        timestamp=cursor.fetchall()
        return(timestamp[0][0])


def get_children_with_pq(transactionid, delai, source_timestamp):
    timestamp = get_timestamp(transactionid) + int(delai)
    children = []
    query = ("SELECT (timestamp - " + source_timestamp + "), transaction, previoustransaction"
             "FROM transactions"
             "WHERE previoustransaction LIKE  '%" + transactionid + "%' and timestamp<" + str(timestamp))
    cursor.execute(query)
    children = cursor.fetchall()
    return children
