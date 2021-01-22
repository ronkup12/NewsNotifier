import requests
from bs4 import BeautifulSoup


class YnetCrawler:
    def __init__(self):
        self.url = "https://www.ynet.co.il/"

    def get_top_story(self):
        top_story_class = "TopStoryComponenta"
        html_doc = requests.get(self.url).content
        soup = BeautifulSoup(html_doc, "html.parser")
        top_story = soup.find(class_=top_story_class).h1
        title = top_story.text
        link = top_story.a["href"]
        subtitle = soup.find(class_=top_story_class).find(class_="slotSubTitle").text
        return (title, subtitle, link)
