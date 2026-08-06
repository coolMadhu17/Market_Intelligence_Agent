"""
markdown_writer.py

Creates one Markdown knowledge file per competitor.

Input:
    self.all_articles

Output:
    output/markdown/
        Bosch.md
        Foxconn.md
        ...

Author : Madhu
"""

import os
from collections import defaultdict
from datetime import datetime


class MarkdownWriter:

    def __init__(self):

        self.output_folder = "output/markdown"

        os.makedirs(self.output_folder, exist_ok=True)

    ##################################################################

    def generate(self, articles):

        if not articles:
            print("No articles available.")
            return

        companies = defaultdict(list)

        # ------------------------------------------------------------
        # Group by Company
        # ------------------------------------------------------------

        for article in articles:

            company = article.get("company", "Unknown")

            companies[company].append(article)

        print(f"Creating markdown for {len(companies)} companies...")

        # ------------------------------------------------------------

        for company, company_articles in companies.items():

            self.write_company_file(
                company,
                company_articles
            )

        print("Markdown generation completed.")

    ##################################################################

    def write_company_file(
            self,
            company,
            articles):

        filename = company.replace("/", "_")

        filepath = os.path.join(
            self.output_folder,
            filename + ".md"
        )

        # ------------------------------------------------------------
        # Group by Keyword
        # ------------------------------------------------------------

        keyword_groups = defaultdict(list)

        for article in articles:

            keyword = article.get(
                "keyword",
                "General"
            )

            keyword_groups[keyword].append(article)

        # ------------------------------------------------------------

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as md:

            md.write("# Competitor Intelligence Report\n\n")

            md.write(f"## Company\n{company}\n\n")

            md.write(
                f"## Generated\n"
                f"{datetime.now():%Y-%m-%d %H:%M}\n\n"
            )

            md.write(
                f"## Total Articles\n"
                f"{len(articles)}\n\n"
            )

            md.write("---\n\n")

            # --------------------------------------------------------

            for keyword in sorted(keyword_groups.keys()):

                md.write(
                    f"# Keyword : {keyword}\n\n"
                )

                group = keyword_groups[keyword]

                # ----------------------------------------------------

                group = sorted(
                    group,
                    key=lambda x: x.get(
                        "published",
                        ""
                    ),
                    reverse=True
                )

                # ----------------------------------------------------

                for index, article in enumerate(
                        group,
                        start=1):

                    md.write(
                        f"## Article {index}\n\n"
                    )

                    md.write(
                        f"**Title**\n"
                        f"{article.get('title','')}\n\n"
                    )

                    md.write(
                        f"**Published**\n"
                        f"{article.get('published','')}\n\n"
                    )

                    md.write(
                        f"**Source**\n"
                        f"{article.get('source','')}\n\n"
                    )

                    md.write(
                        f"**Summary**\n"
                        f"{article.get('summary','')}\n\n"
                    )

                    md.write(
                        f"**URL**\n"
                        f"{article.get('url','')}\n\n"
                    )

                    md.write(
                        "---\n\n"
                    )

            md.write("\n")