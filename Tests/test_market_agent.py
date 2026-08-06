import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from analysis.market_agent import MarketAgent
from analysis.llm_analyzer import LLMAnalyzer
from rag.retriever  import MarketRetriever

retriever = MarketRetriever()

llm = LLMAnalyzer()

agent = MarketAgent(
    retriever=retriever,
    llm=llm
)
print("Call before LLM")
response = agent.run(
    company="Jabil",
    k=4
)

print(response)