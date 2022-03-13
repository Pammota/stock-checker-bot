import requests
import unidecode
from bs4 import BeautifulSoup
from bs4 import Comment
import time
from emailer import email
from email_list import emailsList, productsList

def getStatus(url):

    try:
        res = requests.get(url)
        html_page = res.content

        soup = BeautifulSoup(html_page, 'html.parser')

        result = soup.find("p", {"id":"availability_statut"})

        raw = result.text
        noacc = unidecode.unidecode(raw) 

        return noacc
    except:
        print("Connection unsuccessful.")
        return False

def getName(url):

    try:
        res = requests.get(url)
        html_page = res.content

        soup = BeautifulSoup(html_page, 'html.parser')

        result = soup.find("h1", {"itemprop":"name"})

        raw = result.text
        noacc = unidecode.unidecode(raw) 

        return noacc
    except:
        print("Connection unsuccessful.")
        return False



def writer(word):
    f = open("status.txt","w")
    f.write(word)
    f.close()

def isInStock(status):
    if("\nAcest produs nu mai este in stoc\n" == status):
        return False
    else:
        return True

def backInner(url):
    return f"""\
Subject: The item {getName(url)} is back in stock!

The item {getName(url)} from the following url is back in stock: \n {url}"""

def outOffer(url):
    return  f"""\
Subject: The item {getName(url)} is out of stock!

The item {getName(url)} from the following url is out of stock: \n {url}"""

class Products:
    def __init__(self, url, hasSentInStock,hasSentNotInStock):
        self.url = url
        self.hasSentInStock = hasSentInStock
        self.hasSentNotInStock = hasSentNotInStock

def objBuilder(pList):
    eList=[]
    for i in range(0,len(pList)):
        Product = Products(pList[i],False,False)
        eList.append(Product)

    return eList



def checkerBot(Product,recEmail,firstRun):
    status = getStatus(Product.url)
    time.sleep(0.3)

    if(type(status) != type("")):
        print("Status was not a string!")
    else:
        if(isInStock(status)):
            if(Product.hasSentInStock == False):
                if(firstRun == False): 
                    email(backInner(Product.url),recEmail)
                Product.hasSentInStock=True
                Product.hasSentNotInStock=False
        else:
            if(Product.hasSentNotInStock == False):
                if(firstRun == False):
                    email(outOffer(Product.url),recEmail)
                Product.hasSentInStock=False
                Product.hasSentNotInStock=True
    

objList = objBuilder(productsList)

firstRun = True
while 1:

    for x in emailsList:
        for y in objList:
            checkerBot(y,x,firstRun)
            
    firstRun = False
    # print(getStatus(productsList[2]))
    # print(getStatus(productsList[5]))

    time.sleep(5)