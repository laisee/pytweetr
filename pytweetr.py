import os
import sys
import json
import requests
import datetime
import time
import tweepy
from time import gmtime, strftime
from exceptions import BaseException
from traceback import format_exc
import commands
import logging

def getXem():

   pair = "BTC_XEM"
   url = "https://poloniex.com/public?command=returnTicker"
   msgs = []
   try:
     r = requests.get(url)
     price = r.json()[pair]["last"]
     msg = "Latest price for %s @ Poloniex is  %s [%s]" % (pair,price,datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S %Z%Y"))
     msgs.append(msg)
   except BaseException as ex:
     print(format_exc())
     return ""   

   return msgs

''' Write Xem details to Twitter using details from getRekage '''
def WriteXem(msgs):

   if msgs is None or len(msgs) == 0: 
     return

   # Consumer keys and access tokens
   app_key             = 'TWITTER_APP_KEY'
   app_secret          = 'TWITTER_APP_SECRET'
   access_token        = 'TWITTER_ACCESS_TOKEN'
   access_token_secret = 'TWITTER_TOKEN_SECRET'

   auth = tweepy.OAuthHandler(app_key,app_secret)
   auth.set_access_token(access_token,access_token_secret)
   api = tweepy.API(auth)
   for msg in msgs:
      try:
         print("Sending twitter update '%s' " % msg)
         api.update_status(msg)
      except BaseException as ex:
         print(format_exc())

if __name__ == "__main__":

   SLEEPTIME = 3600 # seconds

   run = None    
   while run != 'n':
      Xem = getXem()
      if Xem:
         WriteXem(Xem)
      print('Sleeping ...')
      time.sleep(SLEEPTIME) 
   print('Closing XEM ...')
