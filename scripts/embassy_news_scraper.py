#!/usr/bin/env python3
#
# embassy_news_scraper.py
#
# VERSION 0.1
#
# LAST EDIT: 2019-09-18
#
# This script extract the basic information of the news articles
# from Chinese embassy websites.
#
##############################################################################
# REQUIRED MODULES
##############################################################################
import re
import requests
import pycountry
from bs4 import BeautifulSoup
from langdetect import detect, DetectorFactory
from datetime import date
##############################################################################
# FUNCTIONS
##############################################################################
def show_help():
    help_text = ("FILE: \t embassy_news_scraper.py\n"
                 "DESC: \t Given the URL of an news article from any Chinese\n"
                 "\t Embassy website, this script outputs the basic\n"
                 "\t information(eg.title, source, publish date, \n"
                 "\t access date, language) of that perticular article.\n"
                 "NOTE: \t Before running, install 'BeautifulSoup', 'langdetect'\n"
                 "\t and 'pycountry' with the commend line arguments \n"
                 "\t [pip install beautifulsoup4],[pip install langdetect]\n"
                 "\t [pip install pycountry].\n"
                 "USGE: \t This script does not handle linkes other than\n"
                 "\t news articles from Chinese Embassy websites.\n"
                 "\t -h, --help   shows the help text\n")
    print(help_text)
##############################################################################
# CLASSES
##############################################################################
class NewsScraper:

    def __init__(self,url):
        #scrap
        self.url = url
        self.request = requests.get(url)
        self.soup = BeautifulSoup(self.request.content, 'html.parser')
        #match the abbreviation given by langdetect with
        #the full name of a language
        self.langs = ['English','Chinese','Spanish']
        self.abbrs = ['en','zh-cn','es']
        self.lang_match = dict(zip(self.abbrs,self.langs))
        #set up the output list
        self.info = [None]*6
        self.info[0] = 'Link:' + self.url

    #title&language
    def __get_title_lang(self):
        #title
        title = self.soup.find('title').get_text()
        self.info[1] = 'Title:' + title
        #language
        DetectorFactory.seed = 0
        self.info[3] = 'Language:' + self.lang_match[detect(title)]

    #publish date
    def __get_publish_date(self):
        self.info[2] = 'Publish Date:' + \
        self.soup.find('div',id='News_Body_Time').get_text()

    #access date
    def __get_access_date(self):
        self.info[4] = 'Access Date:' + date.today().strftime("%Y/%m/%d")

    #publisher
    def __get_source(self):
        abbr = self.url[7:9]
        country = pycountry.countries.get(alpha_2=abbr.upper())
        self.info[5] = 'Source:' + 'Chinese Embassy in ' + country.name

    #get a list representation of the information needed
    #for this article
    def get_info(self):
        self.__get_title_lang()
        self.__get_publish_date()
        self.__get_access_date()
        self.__get_source()
        return "\n".join(self.info)

##########################################################################
# MAIN
##########################################################################
if __name__ == '__main__':

    #take in the url
    inp = input('Enter the URL of your article:')

    #check if the link is valid
    if not re.search('http[s]?://\w\w.china-embassy|chineseembassy.org',inp):
        if (inp == '-h') or (inp == '--help'):
            show_help()
        else:
            print('Invalid URL. This script only handles URL from '
            'Chinese Embassy websites.')
    else:
        print(NewsScraper(inp).get_info())
