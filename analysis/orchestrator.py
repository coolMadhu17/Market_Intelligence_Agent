"""
orchestrator.py

Coordinates the end-to-end Market Intelligence V1 workflow.

Author : Madhu
Version : 1.0
"""

import logging
from pathlib import Path

from analysis.market_agent import MarketAgent
from analysis.report_generator import ReportGenerator
from analysis.excel_writer import ExcelWriter


logger = logging.getLogger(__name__)


class MarketIntelligenceOrchestrator:
    """
    Coordinates:

        Retriever
            ↓
        MarketAgent
            ↓
        ReportGenerator
            ↓
        ExcelWriter
    """

    def __init__(
        self,
        market_agent: MarketAgent,
        report_generator: ReportGenerator,
        excel_writer: ExcelWriter,
    ) -> None:

        self.market_agent = market_agent
        self.report_generator = report_generator
        self.excel_writer = excel_writer

    # ------------------------------------------------------------------

    def run(
        self,
        company: str,
        question: str = "",
        k: int = 1,
        filename: str | None = None,
    ) -> Path:
        """
        Generate a complete Market Intelligence report.

        Parameters
        ----------
        company : str
            Competitor company to analyze.

        question : str
            Optional custom analysis question.

        k : int
            Number of documents retrieved for the LLM.

        filename : str | None
            Optional Excel filename.

        Returns
        -------
        Path
            Path to the generated Excel report.
        """

        logger.info(
            "Starting Market Intelligence workflow: %s",
            company
        )

        # --------------------------------------------------------------
        # 1. Market Agent
        # --------------------------------------------------------------

        raw_response = self.market_agent.run(
            company=company,
            question=question,
            k=k,
        )

        logger.info(
            "Market Agent completed: %s",
            company
        )

        # --------------------------------------------------------------
        # 2. Report Generator
        # --------------------------------------------------------------

        report = self.report_generator.generate(
            raw_response
        )

        logger.info(
            "Report generated: %s",
            company
        )

        # --------------------------------------------------------------
        # 3. Excel Writer
        # --------------------------------------------------------------

        output_path = self.excel_writer.write(
            report=report,
            filename=filename,
        )

        logger.info(
            "Excel report created: %s",
            output_path
        )

        return output_path