

import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))
from analysis.excel_writer import ExcelWriter
from analysis.report_generator import ReportGenerator

writer = ExcelWriter()



sample_json = """
{
    "company": "Jabil",

    "executive_summary": {
        "overview": "Jabil is expanding manufacturing capacity in India.",
        "sentiment": "Positive",
        "confidence": 0.92
    },

    "events": [
        {
            "title": "Jabil expands Pune manufacturing facility",
            "summary": "Jabil announced expansion of its India manufacturing operations.",
            "event_type": "Expansion",
            "importance": "High",
            "business_impact": "Higher manufacturing capacity.",
            "source": "Google News",
            "url": "https://example.com/article",
            "published": "2026-06-19T07:00:00+00:00",
            "sentiment": "Positive",
            "confidence": 0.91
        }
    ],

    "risks": [
        {
            "description": "Execution risk during capacity expansion.",
            "severity": "Medium",
            "impact": "Possible delays in ramp-up.",
            "mitigation": "Monitor expansion milestones.",
            "confidence": 0.80
        }
    ],

    "recommendations": [
        {
            "priority": "High",
            "recommendation": "Monitor Jabil's India expansion closely.",
            "rationale": "Expansion may create future EMS opportunities."
        }
    ],

    "sources": [
        {
            "title": "Jabil Expands India Operations",
            "source": "Google News",
            "url": "https://example.com/article",
            "published": "2026-06-19T07:00:00+00:00",
            "summary": "Jabil expands manufacturing operations in India.",
            "keyword": "expansion"
        }
    ]
}
"""


generator = ReportGenerator()

report = generator.generate(sample_json)

output_path = writer.write(report)

print("Excel created:")
print(output_path)