
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from analysis.report_generator import ReportGenerator


sample_json = """
{
    "company": "Kaynes Technology",
    "executive_summary": {
        "overview": "Kaynes Technology is executing a clear strategy of expansion, significantly broadening its industrial scope and global presence. Key strategic moves include entering the Aerospace sector through targeted acquisitions, strengthening its domestic semiconductor ecosystem via international partnerships (Taiwan), and building out advanced manufacturing capabilities with an OSAT facility in Telangana. These developments signal aggressive growth and diversification across high-tech sectors.",
        "sentiment": "Positive",
        "confidence": 0.9
    },
    "events": [
        {
            "title": "Global Expansion and Aerospace Sector Entry",
            "summary": "Kaynes Technology is expanding its global footprint through targeted acquisitions, specifically entering the Aerospace sector. The company also reportedly expanded its global reach with a Canadian acquisition, alongside reporting strong Q1 results.",
            "event_type": "Acquisition",
            "importance": "Critical",
            "business_impact": "This expansion drastically diversifies Kaynes' service portfolio beyond traditional EMS into high-value sectors like Aerospace and Semiconductors. The acquisitions suggest maturing capabilities to handle complex, specialized electronics manufacturing for premium markets.",
            "source": "Google News RSS / scanx.trade (Merged)",
            "url": "https://news.google.com/rss/articles/... (Acquisitions URL)/https://news.google.com/rss/articles/... (scanx.trade URL)",
            "published": "2025-07-30T07:00:00+00:00",
            "sentiment": "Positive",
            "confidence": 0.9
        },
        {
            "title": "Initi"
"""
generator = ReportGenerator()

report = generator.generate(sample_json)

print()
print("Company:", report.company)
print("Report Date:", report.report_date)
print("Summary:", report.executive_summary.overview)
print("Events:", len(report.events))
print("Risks:", len(report.risks))
print("Recommendations:", len(report.recommendations))
print("Sources:", len(report.sources))
print("Event Type:", report.events[0].event_type)
print("Importance:", report.events[0].importance)
print("Business Impact:", report.events[0].business_impact)