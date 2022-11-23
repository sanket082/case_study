import json
from collections import deque
from bs4 import BeautifulSoup
import urllib.parse as urlparse
import keywords
import csv

import urllib.request as urllib2


#assign url
url = "https://www.homedepot.com/"


# we are performing a bfs crawl by looking at each link on a page and adding them to a queue
bfsQueue = deque([])

# Maintains list of visited pages
visited = []


# Crawl the page and populate the queue with newly found URLs
def bfsSearch(url):
    visited.append(url)
    if len(bfsQueue) > 150:
        return

    urlf = urllib2.urlopen(url)
    soup = BeautifulSoup(urlf.read(),features="html.parser")
    urls = soup.findAll("a", href=True)

    for i in urls:
        flag = 0
        # Complete relative URLs and strip trailing /
        complete_url = urlparse.urljoin(url, i["href"]).rstrip('/').split('#')[0]

        # Check if the URL already exists in the queue
        for j in bfsQueue:
            if j == complete_url:
                flag = 1
                break

        # If not found in queue
        if flag == 0:
            if len(bfsQueue) > 150:
                return
            # check if the link is not in visited and is a link for product(containg /p/)
            if (visited.count(complete_url)) == 0 and "/p/" in complete_url:
                bfsQueue.append(complete_url)

    # Pop one URL from the queue from the left side so that it can be crawled

    current = bfsQueue.popleft()
    # Recursive call to crawl until the queue is populated with 100 URLs
    bfsSearch(current)

bfsSearch(url)

titles=[]
price=[]
d1 = []
keyw = []
flag=0
for i in bfsQueue:
    if flag>100:
        break
    urlf = urllib2.urlopen(i)
    soup = BeautifulSoup(urlf.read(),features="html.parser")
    try:
        titles.append(str(soup.find_all("h1", class_="product-details__title")).split('>')[1].split("<")[0])
        temp = str(soup.find_all("div", class_="price-format__large price-format__main-price")).split("$")[1]
        price.append("$"+temp.split("<span>")[1].split("</span>")[0]+"."+ temp.split("<span class=\"price-format__large-symbols\">")[1].split("</span>")[0])
        # d1.append(str(soup.find_all("div", class_="price-format__large price-format__main-price")))
        d1.append(str(json.loads(soup.find('script', type="application/ld+json").text)["description"]))
        flag+=1
    except:
        flag-=1
        continue
for i in d1:
    keyw.append(keywords.key(i))


with open('data2.csv', "w") as f:
    writer = csv.writer(f)
    writer.writerow(["Title","Price","Keywords"])
    for i in range(len(titles)):
        try:
            writer.writerow([titles[i],price[i],keyw[i][0]+", "+keyw[i][1]+", "+keyw[i][2]])
        except:
            continue