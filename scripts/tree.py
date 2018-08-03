# -*- coding: utf8 -*-
import os
from time import *
import subprocess
import re
import json
from collections import Counter
import mysql.connector

BITCOIND_PATH = '/home/abrochec/blockchain/bitcoin-0.16.1'

cnx = mysql.connector.connect(user='root', password='Alexis2018!',host='localhost',database='miners') #10
cursor = cnx.cursor()


def get_children(transactionid, delai):
        children=[]
        timestamp = get_timestamp(transactionid) + delai
        query=("SELECT transaction, timestamp FROM transactions WHERE previoustransaction LIKE  '"+transactionid+"' and timestamp<"+str(timestamp))
        cursor.execute(query)
        children=cursor.fetchall()
        return(children)

def get_timestamp(transactionid):
        timestamp=[]
        query=("SELECT timestamp FROM transactions WHERE transaction LIKE  '"+transactionid+"'")
        cursor.execute(query)
        timestamp=cursor.fetchall()
        return(timestamp[0][0])

