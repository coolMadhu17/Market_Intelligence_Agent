"""
Google News RSS Collector

Author : Madhu

Free Source:
https://news.google.com/rss

"""



import xml
import logging
import os   
import time
import json
import requests
import feedparser
from bs4 import BeautifulSoup
from urllib.parse import quote
from collectors.base_collector import BaseCollector


class GoogleNewsCollector(BaseCollector):


    BASE_URL = "https://news.google.com/rss/search?q="

    def __init__(self):
        super().__init__("GoogleRSS")

        self.logger = logging.getLogger("MarketIntel")

        os.makedirs("output/raw", exist_ok=True)

    ##############################################################

    def build_query(self, company, keyword):

        query = f'"{company}" {keyword}'

        return query

    ##############################################################

    def build_url(self, company, keyword):

        query = self.build_query(company, keyword)

        return self.BASE_URL + quote(query)

    ##############################################################

    def clean_html(self, text):

        if text is None:
            return ""

        soup = BeautifulSoup(text, "html.parser")

        return soup.get_text(" ", strip=True)

    ##############################################################

    def normalize_article(
        self,
        company,
        keyword,
        entry
    ):

        summary = ""

        if "summary" in entry:

            summary = self.clean_html(entry.summary)

        article = {

            "company": company,

            "keyword": keyword,

            "title": entry.title,

            "summary": summary,

            "url": entry.link,

            "published": entry.get(
                "published",
                ""
            ),

            "source": "Google News RSS"

        }

        return article

    ##############################################################

  
    ##############################################################

    def search(
        self,
        company,
        keyword,
        retries=3
    ):

        url = self.build_url(
            company,
            keyword
        )

        self.logger.info(
            "Google RSS : %s",
            url
        )

        for attempt in range(retries):

            try:

               xml = self.get(url)
               if xml is None:
                    return []

               feed = feedparser.parse(xml)
               articles = []
               for entry in feed.entries:

                    article = self.normalize_article(
                        company,
                        keyword,
                        entry
                    )

                    articles.append(article)

               articles = self.remove_duplicates(
                    articles
                )

               self.save_json(
                    company,
                    keyword,
                    articles
                )

               self.logger.info(
                    "%s + %s -> %d articles",
                    company,
                    keyword,
                    len(articles)
                )

               return articles

            except Exception as ex:

                self.logger.warning(
                    "Retry %d : %s",
                    attempt + 1,
                    ex
                )

                time.sleep(2)

        self.logger.error(
            "Failed Google RSS : %s %s",
            company,
            keyword
        )

        return []