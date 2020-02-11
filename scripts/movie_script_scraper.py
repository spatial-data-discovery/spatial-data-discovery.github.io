#Jenna Ollen
#
#movie_script_scraper.py
#
#VERSION 1.0
#
#LAST EDIT: 2020-02-10
#
#This code scrapes movie scripts from Scripts.com and saves the text in a .txt file.
#It has two optional parameters: a path to save the .txt file and a scripts.com link.
#Some of the code was given to me in Professor Dan Parker's LING 380 Class
#in the SPRING 2019 and adapted by me.
#
#########################################
#REQUIRED MODULES
#########################################
import argparse
import requests
import re
import os

from urllib.request import urlopen
from bs4 import BeautifulSoup

#########################################
#FUNCTIONS
#########################################
def pullText(link):
    session = requests.Session()
    page_response = session.get(link)
    page_content = BeautifulSoup(page_response.content, 'html.parser')
    page_text = page_content.find_all('p')
    clean=re.sub('<[^>]*>', '', str(page_text))
    return (str(clean))

def fileCreate(path_name,script_name):
    name=re.findall("https://www.scripts.com/script/(.*)\_[0-9]", script_name)
    with open(os.path.join(path_name, name[0]+'.txt'), 'w+') as file:
        file.write(pullText(script_name))
    return

#########################################
#MAIN
#########################################
# Check command-line arguments
p = argparse.ArgumentParser(description="This code scrapes movie scripts from Scripts.com and saves the text in a .txt file." )
p.add_argument("-p", "--path", default=".",
                help="Path to save .txt file")
p.add_argument("--link", default="https://www.scripts.com/script/a_cinderella_story_5578",
                help="Link to script.com link to movie script")
args = p.parse_args()
fileCreate(args.path,args.link)
