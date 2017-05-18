# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 08:23:21 2017

@author: tomas
"""

from bs4 import BeautifulSoup
import urllib 
from datetime import datetime
import csv
import sys
import os
import smtplib
import lxml
import urllib.request
import re


BASE_URL = ('http://littleguy.vanillaforums.com/categories/used-little-guys-for-sale')
def parse_results():
  souce = urllib.request.urlopen(BASE_URL).read()
  soup = BeautifulSoup(souce,'lxml')
  results = []
  postings = soup.find_all("td", class_='DiscussionName')
  tuples = re.findall(r'href="(.+?)">(.+?)</a>',str(postings))
  for item in tuples:
    results.append({'url': item[0], 'title': item[1]})
  return results

def write_results(results):
    """Writes list of dictionaries to file."""
    fields = results[0].keys()
    with open('littleguy.csv', 'w') as f:
        dw = csv.DictWriter(f, fieldnames=fields, delimiter='|')
        dw.writer.writerow(dw.fieldnames)
        dw.writerows(results)

def has_new_records(results):
    current_posts = [x['url'] for x in results]
    fields = results[0].keys()
    if not os.path.exists('littleguy.csv'):
        return True

    with open('littleguy.csv', 'r') as f:
        reader = csv.DictReader(f, fieldnames=fields, delimiter='|')
        seen_posts = [row['url'] for row in reader]

    is_new = False
    for post in current_posts:
        if post in seen_posts:
            pass
        else:
            is_new = True
    return is_new

def send_text(phone_number, msg):
    fromaddr = "Littleguy Checker"
    toaddrs = str(phone_number) + "@tmomail.net"
    msg = ("From: {0}\r\nTo: {1}\r\n\r\n{2}").format(fromaddr, toaddrs, msg)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login('name@gmail.com', 'bnqnqrzyyaewzwqr')
    server.sendmail(fromaddr, toaddrs, msg)     
    server.sendmail(fromaddr, 'name@gmail.com', msg)
    server.sendmail(fromaddr, 'name2@gmail.com', msg)
    server.quit()

def get_current_time():
    return datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':

    results = parse_results()
    
    # Send the SMS message if there are new results
    if has_new_records(results):
        message = "Hey - there are new littleguy postings"
        PHONE_NUMBER = 8888888888
        print ("[{0}] There are new results - sending text message to {1}".format(get_current_time(), PHONE_NUMBER))
        send_text(PHONE_NUMBER, message)
        write_results(results)
    else:
        print ("[{0}] No new results - will try again later".format(get_current_time()))
        
  
