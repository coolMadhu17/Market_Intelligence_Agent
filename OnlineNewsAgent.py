"""
Market Intelligence Agent

Version : 1.0

Author : Madhu

"""



from utils.config import Config
from utils.logger import setup_logger
from utils.helpers import ensure_directories
from collectors.google_news import GoogleNewsCollector
from processing.markdown_writer import MarkdownWriter
from analysis.llm_analyzer import LLMAnalyzer
from analysis.market_agent import MarketAgent
from analysis.report_generator import ReportGenerator
from analysis.excel_writer import ExcelWriter
from analysis.orchestrator import MarketIntelligenceOrchestrator
from analysis.llm_analyzer import LLMAnalyzer
from rag.retriever import MarketRetriever
from rag.document_loader import DocumentLoader
from rag.vector_store import MarketVectorStore

class OnlineNewsAgent:

    def __init__(self):

        ensure_directories()

        self.logger = setup_logger()

        self.config = Config()
        self.google = GoogleNewsCollector()
        self.all_articles = []

    def load_configuration(self):

        self.logger.info("Loading configuration...")

        self.companies = self.config.get_competitors()

        self.keywords = self.config.get_keywords()

        self.sources = self.config.get_sources()

        self.logger.info(
            "%d competitors loaded",
            len(self.companies)
        )

        self.logger.info(
            "%d keywords loaded",
            len(self.keywords)
        )

        self.logger.info(
            "%d sources configured",
            len(self.sources)
        )

    def display_search_plan(self):

        print()

        print("=" * 60)

        print("Today's Search Plan")

        print("=" * 60)

        for _, company in self.companies.iterrows():

            for _, keyword in self.keywords.iterrows():

                print(
                    f"{company['Company']}  +  {keyword['Keyword']}"
                )

        print()
    def collect_google_news(self):

        self.logger.info("Starting Google News Collection")

        for _, company in self.companies.iterrows():

            company_name = company["Company"]

            for _, keyword in self.keywords.iterrows():

                keyword_name = keyword["Keyword"]

                articles = self.google.search(
                    company_name,
                    keyword_name
             )
                self.all_articles.extend(articles)
                self.logger.info(
                    "%s + %s -> %d articles",
                    company_name,
                     keyword_name,
                    len(articles)
                )

            self.logger.info("Google News Collection Completed")
    def create_markdown_files(self):
        print(f"Total Articles : {len(self.all_articles)}")
        writer = MarkdownWriter()
        writer.generate(self.all_articles)

    def analyze_market_intelligence(self):

         analyzer = LLMAnalyzer()

         analyzer.analyze_all()
         self.logger.info("Market Intelligence Analysis Completed")

    def generate_market_intelligence_reports(self):

        self.logger.info(
            "Generating Market Intelligence Reports..."
        )

        # ---------------------------------------------------------
        # Create dependencies
        # ---------------------------------------------------------

        retriever = MarketRetriever()

        llm = LLMAnalyzer()

        market_agent = MarketAgent(
            retriever=retriever,
            llm=llm
        )

        report_generator = ReportGenerator()

        excel_writer = ExcelWriter()

        orchestrator = MarketIntelligenceOrchestrator(
            market_agent=market_agent,
            report_generator=report_generator,
            excel_writer=excel_writer
        )

        # ---------------------------------------------------------
        # Generate report for every competitor
        # ---------------------------------------------------------

        for _, company in self.companies.iterrows():

            company_name = company["Company"]

            self.logger.info(
                "Generating report for %s",
                company_name
            )

            orchestrator.run(
                company=company_name,
                k=1
            )

        self.logger.info(
            "Market Intelligence Reports Completed"
        )

    def update_vector_database(self):

        loader = DocumentLoader()

        chunks = loader.load_folder()

        current_companies = {
            article["company"]
            for article in self.all_articles
        }

        chunks = [
            chunk
            for chunk in chunks
            if chunk.company in current_companies
        ]

        vector_store = MarketVectorStore()

        vector_store.add_chunks(chunks)

    def run(self):

        self.logger.info("Starting Online News Agent")

        self.load_configuration()

        self.display_search_plan()

        self.collect_google_news()

        self.create_markdown_files()

        #self.analyze_market_intelligence()
       # self.update_vector_database()

        self.generate_market_intelligence_reports()

        self.logger.info("All modules completed successfully")


if __name__ == "__main__":

    agent = OnlineNewsAgent()

    agent.run()