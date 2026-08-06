"""
prompts.py

Prompt templates used by the
Taksa Market Intelligence Agent.

Author : Madhu
Version : 1.0
"""

from datetime import datetime
from typing import List

from langchain_core.documents import Document


###############################################################################
# SYSTEM PROMPT
###############################################################################

SYSTEM_PROMPT = """
You are a Senior Market Intelligence Analyst specializing in the
Electronics Manufacturing Services (EMS) industry.

Your responsibility is to analyze competitor information and generate
actionable business intelligence.

Focus on:

• Manufacturing expansion
• Manufacturing capacity
• Factory openings and closures
• Investments
• Acquisitions and mergers
• Strategic partnerships
• New customers
• Customer losses
• Product launches
• Hiring and layoffs
• Supply chain developments
• Business risks
• Growth opportunities

Think like a:

• CEO
• Head of Strategy
• Sales Director
• Supply Chain Director
• Procurement Head

Do not simply summarize the source material.

For every important finding, determine:

1. What happened?
2. Why is it important?
3. What is the business impact?
4. What risks are visible?
5. What opportunities are visible?
6. What action should be considered?

IMPORTANT RULES:

• Use only information contained in the supplied knowledge.
• Do not invent facts.
• Do not assume facts that are not explicitly supported.
• Do not create URLs or dates that are not present.
• If information is insufficient, say so.
• Merge multiple documents describing the same event.
• Prioritize recent and significant developments.
• Distinguish facts from reasonable interpretation.
"""


###############################################################################
# ARTICLE RELEVANCE RULES
###############################################################################

ARTICLE_RELEVANCE_RULES = """
ARTICLE RELEVANCE RULES

Include ONLY information directly related to the target company.

Discard articles that:

• Mention similar words but refer to another company.
• Are unrelated to the target company.
• Are opinion pieces with no business impact.
• Are duplicate reports of the same event.
• Have no strategic value for an EMS company.

Examples of unrelated articles:

Amazon Flex ≠ Flextronics
Flex Fuel ≠ Flextronics
Flexible Packaging ≠ Flextronics

Only include events that have direct business significance for the target company.

If an article is unrelated, ignore it completely.

Do NOT include unrelated articles in:

• events
• risks
• recommendations
• sources

If multiple articles describe the same event:

• Merge them into one event.
• Keep the best source.
• Do not create duplicate events.
"""


###############################################################################
# OUTPUT FORMAT
###############################################################################

OUTPUT_FORMAT = """
Return ONLY a valid JSON object.

Do NOT return:

- Markdown
- Code fences
- Explanations
- Reasoning
- <think>...</think> blocks
- Notes before or after the JSON

The first character of your response MUST be '{'
The last character of your response MUST be '}'

Every field defined in the JSON schema MUST be present.

If a value is unavailable:

- Use "" for strings.
- Use [] for arrays.
- Use 0.0 for confidence values.

Never omit a field.

Return exactly this structure:

{
    "company": "",

    "executive_summary": {
        "overview": "",
        "sentiment": "Neutral",
        "confidence": 0.0
    },

    "events": [
        {
            "title": "",
            "summary": "",
            "event_type": "Other",
            "importance": "Medium",
            "business_impact": "",
            "source": "",
            "url": "",
            "published": "",
            "sentiment": "Neutral",
            "confidence": 0.0
        }
    ],

    "risks": [
        {
            "description": "",
            "severity": "Medium",
            "impact": "",
            "mitigation": "",
            "confidence": 0.0
        }
    ],

    "recommendations": [
        {
            "priority": "Medium",
            "recommendation": "",
            "rationale": ""
        }
    ],

    "sources": [
        {
            "title": "",
            "source": "",
            "url": "",
            "published": "",
            "summary": "",
            "keyword": ""
        }
    ]
}

ENUM VALUES:

event_type:
Expansion
Investment
Partnership
Acquisition
Product Launch
Customer Win
Customer Loss
Factory
Hiring
Layoff
Legal
Financial
Supply Chain
Other

importance:
Low
Medium
High
Critical

sentiment:
Positive
Negative
Neutral
Mixed

severity:
Low
Medium
High
Critical

priority:
Critical
High
Medium
Low

ENUM RULES

Use ONLY the values listed below.

Do NOT invent new values.

Examples of INVALID values:

"Medium (Indirect)"
"Very High"
"P1"
"P2"
"Moderate"
"Positive/Neutral"

Choose the closest valid enum instead.


CONFIDENCE:

0.9–1.0
Directly supported by multiple articles.

0.7–0.89
Clearly supported by one article.

0.4–0.69
Inference with moderate evidence.

0.0–0.39
Weak evidence.

Never assign 1.0 unless the evidence is overwhelming.

DATE FORMAT:

Use ISO-8601 format whenever a publication date is known.
Example:
2026-06-19T07:00:00+00:00
DATE RULES

Return ONLY an ISO-8601 datetime.

Examples of VALID values:

2026-06-19T07:00:00+00:00

2019-07-17T07:00:00+00:00

Examples of INVALID values:

Wed, 17 May 2017 07:00:00 GMT

Wed, 17 May 2017 07:00:00 GMT (2017-05-17T07:00:00+00:00)

Yesterday

Last Week

Unknown

1 January 2024 (likely referring...)

If the date is unavailable, return:

"published": ""

Do NOT add explanations.
Do NOT include RFC822 dates.
Return ISO-8601 only.


"""


###############################################################################
# BUILD CONTEXT
###############################################################################

def build_context(
    documents: List[Document]
) -> str:
    """
    Convert retrieved LangChain Documents into
    structured context for the LLM.

    Parameters
    ----------
    documents : List[Document]
        Documents retrieved from Chroma.

    Returns
    -------
    str
        Formatted RAG context.
    """

    if not documents:
        return "No relevant documents were retrieved."

    sections = []

    for index, document in enumerate(
        documents,
        start=1
    ):

        metadata = document.metadata or {}

        company = metadata.get(
            "company",
            "Unknown"
        )

        source_file = metadata.get(
            "source_file",
            "Unknown"
        )

        chunk_number = metadata.get(
            "chunk_number",
            ""
        )

        keyword = metadata.get(
            "keyword",
            ""
        )

        article_title = metadata.get(
            "article_title",
            ""
        )

        published = metadata.get(
            "published",
            ""
        )

        url = metadata.get(
            "url",
            ""
        )

        content = document.page_content.strip()

        section = f"""
========================================================================
DOCUMENT {index}
========================================================================

Company      : {company}
Source File  : {source_file}
Chunk        : {chunk_number}
Keyword      : {keyword}
Title        : {article_title}
Published    : {published}
URL          : {url}

CONTENT
-------

{content}
"""

        sections.append(section)

    return "\n".join(sections)


###############################################################################
# BUILD MARKET PROMPT
###############################################################################

def build_market_prompt(
    company: str,
    documents: List[Document],
    question: str = ""
) -> str:
    """
    Build the complete Market Intelligence prompt.

    Parameters
    ----------
    company : str
        Competitor company to analyze.

    documents : List[Document]
        Retrieved RAG documents.

    question : str
        Optional custom analysis question.

    Returns
    -------
    str
        Complete prompt for the LLM.
    """

    if not question:

        question = (
            "Generate today's Market Intelligence Report "
            f"for {company}."
        )

    context = build_context(documents)

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    prompt = f"""
{SYSTEM_PROMPT}


=======================================================================
REPORT DATE
=======================================================================

{today}

=======================================================================
COMPANY
=======================================================================

{company}

=======================================================================
ANALYSIS REQUEST
=======================================================================

{question}

=======================================================================
RETRIEVED KNOWLEDGE
=======================================================================

{context}

=======================================================================
ANALYSIS INSTRUCTIONS
=======================================================================

Analyze the retrieved knowledge carefully.

Identify the most important:

• Business events
• Strategic developments
• Risks
• Opportunities
• Recommended actions

When several documents refer to the same event:

• Treat them as one event.
• Prefer the most complete information.
• Do not artificially increase importance because the same event
  appears multiple times.

Only report information that is supported by the retrieved knowledge.

Do not invent facts.

{OUTPUT_FORMAT}
"""

    return prompt