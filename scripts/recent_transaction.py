# -*- coding: utf8 -*-
import json
import subprocess
import mysql.connector
from inputs_outputs import *

BITCOIND_PATH = '/home/wtan/bitcoin-0.16.0'

#function used to ask the user for the transaction id///////////////
def asktxid():
    txid = input ("Please enter the starting transaction id :")
    return txid

def getheightfromtxid(txid):
    cnx = mysql.connector.connect(user='root', password='William2018!', host='localhost', database='blockchain')

    cursor = cnx.cursor()
    query_height = ("SELECT height FROM heighttxid WHERE txid = %s")
    data_txid = txid
    cursor.execute(query_height, (data_txid,))

    fetchedheight = cursor.fetchone()

    if fetchedheight[0] is not None:
        height=fetchedheight[0]
    else:
        return None

    cursor.close()
    cnx.close()

    return height

def gettimestampfromtxid(txid):
    height = getheightfromtxid(txid)
    blockhash = getblockhashfromheight(height)
    block = getblockfromblockhash(blockhash)

    jsonblock = json.loads(block)

    return jsonblock["time"]

def getlasttransaction(txid):
    comparator=0
    listoflasttransactions =[] #list of the previous transaction

    rawtransaction = getrawtransactionfromtransactionid(txid)
    decodedtransaction = decoderawtransactionfromrawtransaction(rawtransaction)

    #Converting the decoding transaction to json
    jsontransaction = json.loads(decodedtransaction)

    #appel de getVin
    if 'txid' in jsontransaction['vin'][0]:
        for j in range(0, len(jsontransaction["vin"])):
            listoflasttransactions.append(jsontransaction["vin"][j]["txid"])

        for j in range(0, len(listoflasttransactions)):
            if gettimestampfromtxid(listoflasttransactions[j]) > comparator:
                comparator = gettimestampfromtxid(listoflasttransactions[j])
                mostrecenttransaction = listoflasttransactions[j]

        return mostrecenttransaction

    else:
        return 0
