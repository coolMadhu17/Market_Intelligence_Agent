import pandas as pd


class Config:

    def __init__(self):

        self.competitors = pd.read_excel(
            "config/competitors.xlsx"
        )

        self.keywords = pd.read_excel(
            "config/keywords.xlsx"
        )

        self.sources = pd.read_excel(
            "config/sources.xlsx"
        )

        self.settings = pd.read_excel(
            "config/settings.xlsx"
        )

    def get_competitors(self):

        return self.competitors[
            self.competitors["Enabled"] == "Yes"
        ]

    def get_keywords(self):

        return self.keywords[
            self.keywords["Enabled"] == "Yes"
        ]

    def get_sources(self):

        return self.sources

    def get_setting(self, parameter):

        row = self.settings[
            self.settings["Parameter"] == parameter
        ]

        if len(row):

            return row.iloc[0]["Value"]

        return None