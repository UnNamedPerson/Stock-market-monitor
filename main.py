import sys
import time
import logging
import os
import smtplib
import requests

## Used to extract the information form HTML Page
import selectorlib

from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
from dotenv import load_dotenv
from bs4 import BeautifulSoup as BS # for the data extraction from HTML



## Port and server definition for the email gateway
port = 587
server = "smtp-mail.outlook.com"


URL_Link = "https://coinmarketcap.com/"
Headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0'}

## file path
currentDir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = currentDir / ".env" # .env file variables
load_dotenv(envars)

currentPrice = 0
previousPrice = 0
 
## Read the variables from the .env file
sender = os.getenv("Email")
senderPassword = os.getenv("Password")
# senderTuple = ("Stock price folder", f"{sender}")

## Defining the function for sending the automated email.
## 2DO TO CHANGE THE VARIABLES AND SOME OF THE METHODS IN THE FUNCTION
def emailToSend(subject, reciever, cryptoName, precentage):

    port = 587
    server = "smtp-mail.outlook.com"

    emailMsg = EmailMessage()
    emailMsg["Subject"] = subject
    emailMsg["From"] = formataddr(("crypto price change", f"{sender}"))
    emailMsg["To"] = reciever
    emailMsg["BCC"] = sender

# .sc-7b3ac367-3 > tbody:nth-child(3) > tr:nth-child(1) > td:nth-child(4) > div:nth-child(1) > span:nth-child(1)
## YAML file usage for reading the html element in the webpage


# 2DO TO CHANGE (DONE)
    emailMsg.set_content(
        f"""\
        ,
        Please note that crypto {cryptoName} has changed with this precentage: {precentage}
        """
    )

## html version of the message
    emailMsg.add_alternative(
        f"""\
        <html>
            <body>
                <p>Hi, </p>
                <p> Please note that <strong> {cryptoName} </strong> has changed with this precentage: <strong> {precentage}  </strong> </p>
            </body>
        </html>
        """,
            subtype="html"
    )

## preparing the email to be sent and logging to the email server.
    with smtplib.SMTP(server, port) as server:
        server.starttls()
        server.login(sender, senderPassword)
        server.sendmail(sender, reciever, emailMsg.as_string())


## The scraping function
def webPageScraping(url):
    ## scrape the webpage of the url
    ## the response alone shows the request's status (i.e., 200 or 404)
    response = requests.get(url, headers=Headers)
    # HTMLSource = response

    ## this returns the HTML encoding of the URL webpage.
    HTMLSource = BS(response.text, 'html')
    # HTMLElement = HTMLSource.find('p', class_ = "sc-65e7f566-0 iPbTJf coin-item-name").text

    ## This line get the HTML element that has the Bitcoin value
    HTMLElement_bitcoin = HTMLSource.find('div', class_ = "sc-b3fc6b7-0").text

    ## USING BEAUTIFULSOUP TO GET THE HTML CONTENT AS ANOTHER WAY OF READING THE HTML CONTENT.
    ## "html5lib" IS THE PARSER TYPE USED TO PARSE THE HTML CONTENT.
    # HTMLSource = BS(response.content, 'html5lib')

    # return HTMLSource.prettify()

    ## Returns the webpage source HTML
    # return HTMLSource
    return HTMLElement_bitcoin

def extractInformation(sourceText):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    extractedValue = extractor.extract(sourceText)["price"]
    return extractedValue

##  2DO DEFINE A FUNCTION FOR BITCOIN PRICE (DONE)
##  AND ANOTHER FUNCTION TO READ THE DATA THERE (DONE)
def calculateThePrecentageDrop(price):
    global previousPrice
    global currentPrice
    previousPrice = currentPrice
    currentPrice = price
    difference = currentPrice - previousPrice
    precentage = difference * 100
    if(precentage > 0.01):
        print ("The precentage is %f" % precentage)


## main program runs here
if __name__=="__main__":
    ## SETTING THE MAIN DIRECTORY MANUALLY (NOT HAVINTG THIS CAUSED ISSUES EARLER
    ## BUT NOW THE EXECUTABLE IS WORKING FINE WITHOUT THIS LINE.)
    # os.chdir(r'C:\Users\abdal\OneDrive\Desktop\desktop of Desktop\github folder\Stock-market-monitor')


## Testing the webpage scrping method
    for i in range(10):
        print(webPageScraping(URL_Link))
        ## Taking the value without the '$'
        priceString = webPageScraping(URL_Link)[1:]
        ## Removing the commas from the price string
        priceWithoutCommas = priceString.replace(",", "")
        calculateThePrecentageDrop(float(priceWithoutCommas))
        time.sleep(60)
        

    # scrapedInformation = webPageScraping(URL_Link)

## printing out a specific information (price) to test the extraction information method
    # print(extractInformation(scrapedInformation))
