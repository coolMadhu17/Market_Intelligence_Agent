import os

from analysis.ollama_client import OllamaClient


class LLMAnalyzer:

    def __init__(self):

        self.client = OllamaClient()

        self.prompt = open(

            "prompts/market_intelligence_prompt.txt",

            encoding="utf-8"

        ).read()

        os.makedirs(

            "output/analysis",

            exist_ok=True

        )

    #####################################################

    def analyze_file(self, markdown_file):

        print(markdown_file)

        report = open(

            markdown_file,

            encoding="utf-8"

        ).read()

        final_prompt = f"""

{self.prompt}

=======================

COMPETITOR REPORT

=======================

{report}

"""

        answer = self.client.ask(final_prompt)

        company = os.path.basename(

            markdown_file

        ).replace(".md", "")

        outfile = os.path.join(

            "output/analysis",

            company + ".md"

        )

        with open(

            outfile,

            "w",

            encoding="utf-8"

        ) as f:

            f.write(answer)

        print(company, "completed")

    #####################################################

    def analyze(
        self,
        prompt: str
    ) -> str:
        """
        Send a prompt to the LLM.

        Parameters
        ----------
        prompt : str

        Returns
        -------
        str
            Raw LLM response.
        """

        return self.client.ask(prompt)

    def analyze_all(self):

        folder = "output/markdown"

        files = [

            f

            for f in os.listdir(folder)

            if f.endswith(".md")

        ]

        for file in files:

            self.analyze_file(

                os.path.join(

                    folder,

                    file

                )
            )