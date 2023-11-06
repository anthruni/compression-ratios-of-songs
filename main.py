import cloudscraper
import requests
from bs4 import BeautifulSoup
import re
import os

def get_lyrics(link):
    scraper = cloudscraper.create_scraper()
    page = scraper.get(link).text
    soup = BeautifulSoup(page, "html.parser")
    
    #div_lyrics = soup.find_all("div", attrs={"data-lyrics-container": "true"})

    div_lyrics = soup.find_all("div", class_=re.compile("Lyrics__Container"))

    total = ""
    for div in div_lyrics:
        div_text = div.get_text()
        text_without_brackets = re.sub(r"<.*?>", "", div_text)
        #print(text_without_brackets)
        total += text_without_brackets

    return total

#I have intentionally left the token in, use it if you want /shrug

token="7yEYoM_ziFaIm4C6dIjomtV9LqQlLhSNO7-ZJBhhKLylXoCmdjjGsk5ZmqEP5GjE"
def get_link():
    query = input("Enter the song name: ")
    
    x = requests.get(f"http://api.genius.com/search?q={query}&access_token={token}").json()
    
    lnk = x["response"]["hits"][0]["result"]["url"]
    x = requests.get(f"https://archive.org/wayback/available?url={lnk}").json()
    #should error handle here
    return x["archived_snapshots"]["closest"]["url"]


link = get_link()

lyrics = get_lyrics(link)

with open("tmp_lyrics", "w") as f:
    f.write(lyrics)

uncompressed = os.popen("du -b tmp_lyrics").read().split()[0]

os.system("compress tmp_lyrics")
compressed = os.popen("du -b tmp_lyrics.Z").read().split()[0]

os.system("rm tmp_lyrics.Z")

print(f"ratio: {int(compressed)/int(uncompressed):.2f}")

with open("lyrics_ratios_log", "a") as f:
    f.write(f"{int(compressed)/int(uncompressed):.2f}|{link}\n")
