import time
import requests
import bs4
import urllib

start_url = "https://en.wikipedia.org/wiki/Special:Random"
target_url = "https://en.wikipedia.org/wiki/Philosophy"

def find_first_link(url):
    response = requests.get(url)
    html = response.text

    soup = bs4.BeautifulSoup(html, 'html.parser')
    content = soup.find(id="mw-content-text").find(class_="mw-parser-output")

    link = None

    for div in content.find_all("p", recursive = False) :
        if div.find("a", recursive = False):
            link = div.find("a", recursive = False).get("href")
            break

    if not link :
        return

    first_link = urllib.parse.urljoin("https://en.wikipedia.org/", link)

    return first_link


def continue_crawl(search_history, target_url, max_steps=25):
    if(search_history[-1] == target_url):
        print("Target URL Reached")
        return False
    if(len(search_history) > max_steps):
        print("Search length exceeded max steps!")
        return False
    if(len(search_history) != len(set(search_history))):
        print("duplicates found!")
        return False
    return True

search_history = [start_url]

while continue_crawl(search_history, target_url):
    print(search_history[-1])
    first_link = find_first_link(search_history[-1])
    if not first_link :
        print("No links found on the page")
        break
    search_history.append(first_link)
    time.sleep(2)
