"""
Base Collector

Common functionality used by all news collectors.

Author : Madhu
"""

import json
import logging
import os
import time

import requests


class BaseCollector:

    def __init__(self, source_name):

        self.source_name = source_name

        self.logger = logging.getLogger("MarketIntel")

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        })

        os.makedirs("output/raw", exist_ok=True)

    ############################################################

    def get(self, url, retries=3):

        for attempt in range(retries):

            try:

                response = self.session.get(
                    url,
                    timeout=30
                )

                response.raise_for_status()

                return response.text

            except Exception as ex:

                self.logger.warning(
                    "%s Retry %d : %s",
                    self.source_name,
                    attempt + 1,
                    ex
                )

                time.sleep(2)

        return None

    ############################################################

    def save_json(
        self,
        company,
        keyword,
        articles
    ):

        filename = (
            f"{company}_{keyword}_{self.source_name}"
        )

        filename = filename.replace(" ", "_")

        filepath = os.path.join(
            "output/raw",
            filename + ".json"
        )

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                articles,
                f,
                indent=4,
                ensure_ascii=False
            )

    ############################################################

    def remove_duplicates(
        self,
        articles
    ):

        urls = set()

        unique = []

        for article in articles:

            if article["url"] not in urls:

                urls.add(article["url"])

                unique.append(article)

        return unique