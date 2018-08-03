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


def get_children(transactionid, timestamp):
        children=[]
        query=("SELECT transaction, timestamp FROM transactions WHERE previoustransaction LIKE  '"+transactionid+"' and timestamp<"+timestamp)
        cursor.execute(query)
        children=cursor.fetchall()
        return(children)

def get_timestamp(transactionid):
        timestamp=[]
        query=("SELECT timestamp FROM transactions WHERE transaction LIKE  '"+transactionid+"'")
        cursor.execute(query)
        timestamp=cursor.fetchall()
        return(timestamp[0][0])

def delai(x):
        return {
                '1': 86400,
                '2': 604800,
                '3': 26280000
        }.get(x, 68400)


transactionid=input("enter the id of the transaction you are looking for :")
timestamp=get_timestamp(transactionid)
choice=input("On which periode do you want to make the studie ? 1: a day  2: a week  3: a month") # le switch marche pas en python
delai=delai(choice)
timestamp=timestamp+delai
print(timestamp)
children=get_children(transactionid,str(timestamp))
print(children)
while True:
        for i in children:
                result=get_children(i[0],str(timestamp))
                children.append(result[0]) #need to find a way to leave the loop
                print(i)
        break
print(children)

