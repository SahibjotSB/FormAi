from bs4 import BeautifulSoup
import requests


URL = "https://www.soccer24.com/match/SxFxJ44k/#/match-summary/match-statistics/0"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
for a_href in soup.find_all("a", href=True):
    print(a_href["href"])