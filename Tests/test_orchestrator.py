import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


from analysis.market_agent import MarketAgent
from analysis.report_generator import ReportGenerator
from analysis.excel_writer import ExcelWriter
from analysis.orchestrator import MarketIntelligenceOrchestrator

from rag.retriever import MarketRetriever
from analysis.llm_analyzer import LLMAnalyzer


# -------------------------------------------------------------------------
# Create dependencies
# -------------------------------------------------------------------------

retriever = MarketRetriever()

llm = LLMAnalyzer()

market_agent = MarketAgent(
    retriever=retriever,
    llm=llm,
)

report_generator = ReportGenerator()

excel_writer = ExcelWriter(
    output_directory="reports"
)


# -------------------------------------------------------------------------
# Create orchestrator
# -------------------------------------------------------------------------

orchestrator = MarketIntelligenceOrchestrator(

    market_agent=market_agent,

    report_generator=report_generator,

    excel_writer=excel_writer,
)


# -------------------------------------------------------------------------
# Run
# -------------------------------------------------------------------------

output_path = orchestrator.run(

    company="Kaynes",

    question=(
        "Generate today's market intelligence report "
        "with emphasis on major strategic and "
        "manufacturing developments."
    ),

    k=1,
)


print()
print("=" * 70)
print("MARKET INTELLIGENCE COMPLETED")
print("=" * 70)
print("Excel Report:")
print(output_path)