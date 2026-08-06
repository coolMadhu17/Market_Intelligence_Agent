"""
market_agent.py

Market Intelligence Agent

Coordinates retrieval, prompt generation and
LLM analysis.

Author : Madhu
Version : 1.0
"""

from urllib import response

from prompts.prompt import build_market_prompt


###############################################################################


class MarketAgent:
    """
    Market Intelligence Agent.
    """

    ###########################################################################

    def __init__(
        self,
        retriever,
        llm,
        logger=None
    ):

        self.retriever = retriever

        self.llm = llm

        self.logger = logger

    ###########################################################################

    def run(
        self,
        company: str,
        question: str = "",
        k: int = 10
    ) -> str:
        """
        Generate a Market Intelligence Report.

        Parameters
        ----------
        company : str
            Company to analyze.

        question : str
            Optional custom question.

        k : int
            Number of RAG documents.

        Returns
        -------
        str
            Raw LLM response (JSON string).
        """

        if self.logger:

            self.logger.info(
                "Starting Market Intelligence Analysis : %s",
                company
            )

        #######################################################################
        # Retrieve documents
        #######################################################################
        
        query = f"""
        {company}

        manufacturing expansion
        capacity
        factory
        investment
        customer
        partnership
        acquisition
        product launch
        hiring
        layoff
        supply chain
        """

        print()
        print("=" * 80)
        print("QUERY SENT TO CHROMA")
        print("=" * 80)
        print(query)
        print("=" * 80)

        documents = self.retriever.company_search(
            company=company,
            query=query,
            k=3
        )
# ADD HERE
        print("=" * 70)
        print(f"Retrieved Documents : {len(documents)}")

        if self.logger:

            self.logger.info(
                "Retrieved %d documents",
                len(documents)
            )

        #######################################################################
        # Build Prompt
        #######################################################################

        prompt = build_market_prompt(
            company=company,
            documents=documents,
            question=question
        )

        if self.logger:

            self.logger.info(
                "Prompt Size : %d characters",
                len(prompt)
            )

        #######################################################################
        # Call LLM
        #######################################################################
# ADD HERE
        print("=" * 70)
        print(f"Prompt Length : {len(prompt):,} characters")
        print(f"Approx Tokens : {len(prompt)//4:,}")

        with open("debug_prompt.txt", "w", encoding="utf-8") as f:
         f.write(prompt)

        print("Prompt saved to debug_prompt.txt")
        print("=" * 70)
        response = self.llm.analyze(prompt)

        print("=" * 70)
        print("RAW LLM RESPONSE")
        print("=" * 70)
        print(response)
        print("=" * 70)




        if self.logger:

            self.logger.info(
                "LLM Response : %d characters",
                len(response)
            )

            self.logger.info(
                "Market Intelligence Completed : %s",
                company
            )

        return response