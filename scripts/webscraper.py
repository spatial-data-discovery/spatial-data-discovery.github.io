#reference_page
#("https://www.digitalocean.com/community/tutorials/how-to-scrape-web-pages-with-beautiful-soup-and-python-3")
#(https://www.guru99.com/reading-and-writing-files-in-python.html)
import requests #making http requests in python
from bs4 import BeautifulSoup #helps with parsing and grabbing info
web_address = "https://www.wm.edu/as/computerscience/undergraduate/major/index.php"
page = requests.get(web_address)

#Creating a soup object

#collect text from page and parse page
soup = BeautifulSoup(page.text, "html.parser")

#Grab info or data from the user_content class div block
cs_text = soup.find(class_ = "user_content")

#Grab text from all instances of <p> tag in the user_content class div block
cs_text_info = cs_text.find_all("p")

#For loop to print out all texts within block
# for text in cs_text_info:
#     print(text.prettify()) #prettify() method helps turned the parsed info into nice unicode string

#.contents pulls out the text found inside the <p> tags
# for text in cs_text_info:
#     information = text.contents[0]
#     print(information)

text_doc = open("scrapedtext.txt", "w+") #creates a new text file
for text in cs_text_info:
    information = text.contents[0]
    text_doc.write(information+"\n")
text_doc.close()
