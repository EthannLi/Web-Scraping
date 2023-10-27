import requests
from pathlib import Path
from datetime import datetime as dt
import json
import bs4


MONTREAL_GAZETTE_URL = "https://montrealgazette.com"
counter = 0
def getNewsLink(url,name):    
    fpath = Path(f"../data/raw_data/trendingLink_{name}.html")
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    
    # Check if the file exists
    if not fpath.exists():    
        # If not, create the file
        trending_List = requests.get(f"{MONTREAL_GAZETTE_URL}{url}", headers=headers)
        with open(fpath, "w") as f:
            f.write(trending_List.text)
    
    with open(fpath) as f:
        return f.read()

def getTrendingListLink():
    links = []  
    html = getNewsLink("/category/news/", dt.now().strftime("%Y-%m-%d"))
    soup = bs4.BeautifulSoup(html, "html.parser")
    caroussel = soup.find("div", {"class": "list-widget list-widget-trending"})
    # print(caroussel)
    
    # Getting all the links for the trending list 

    list_Item = caroussel.find_all("li")
    for item in list_Item:
        # print("link")
        link = item.find("a",{"class":"article-card__link"})
        links.append(link["href"])  
    return links

def getInfoFromLink(data,link):

    # Setups

    global counter
    html = getNewsLink(link,counter)
    soup = bs4.BeautifulSoup(html,"html.parser")

    header = soup.find("div",{"class": "article-header__detail__texts"})
    # Title

    title = header.find("h1",id= "articleTitle").text
    # print(title)

    # Publication date
    publication_date = header.find("span", {"class": "published-date__since"}).text
    print(publication_date)

    # Author
    authorSpan = header.find("span",{"class":"published-by__author"})
    author = authorSpan.find("a").text
    # print(author)

    # Blurb
    blurb = header.find("p",{"class":"article-subtitle"}).text
    # print(blurb)
    createData(data,title,publication_date,author,blurb)
    counter += 1

def createData(data,title,publication_date,author,blurb):
    # Create a JSON file with the data
    # List of all trending news
    data.append({
        "title": title,
        "publication_date": publication_date,
        "author": author,
        "blurb": blurb
    })

    
def createJSON(name):
    data = []
    fpath = Path(f"../data/output_data/{name}")

    for link in getTrendingListLink():
        print("\n")
        getInfoFromLink(data,link)
    
    
    with open(fpath, "w") as f:
        json.dump(data, f, indent=4)
