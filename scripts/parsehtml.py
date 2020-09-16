import urllib.request, json, re, argparse #re needed to replace whitespace down the line
from bs4 import BeautifulSoup

def parsehtml(url):
    with urllib.request.urlopen(url) as req:
        contents = req.read() #this will be all the text
    soup = BeautifulSoup(contents, features='html.parser') 
    text = soup.find_all(['p','h2']) #I want all text in paragraphs (p) and headings (h2)
    review = []
    for i in text:
        if i.name == 'h2': #I want a colon after every heading to make sentences clearer.
            review.append(i.get_text(strip=True)+':') #get_text() gives a str, which allows concat with ":"
        else:
            review.append(i.get_text(strip=True)) #if not h2, do nothing
    review_cleaned = [re.sub("\s+"," ",rev) for rev in review] #changes all whitespace to single space
    #review_cleaned = review_cleaned[:-5] #the last elements are not important: "thanks for reading" etc
    review_txt = " ".join(review_cleaned) #make list into one long str to be written in
    with open("Output.txt", "w") as txtfile:
        txtfile.write(review_txt)
	txtfile.write('\n')
    return "done"

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='scrape a simple html website by adding the url after py file name. You MUST have bs4 installed!')
    parser.add_argument('website',type=str, metavar='',help='input your website here')
    args = parser.parse_args()

    print(parsehtml(args.website))
