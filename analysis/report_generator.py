"""
report_generator.py

Converts raw JSON returned by the LLM into
a typed MarketIntelligenceReport.

Author : Madhu
Version : 1.0
"""

import json
from datetime import datetime
from typing import Any, Type, TypeVar

from google_crc32c import value
from sqlalchemy import text
import re
from json_repair import repair_json

from models.models import (
    EventType,
    ExecutiveSummary,
    Importance,
    MarketEvent,
    MarketIntelligenceReport,
    Priority,
    Recommendation,
    Risk,
    RiskSeverity,
    Sentiment,
    SourceArticle,
)


EnumType = TypeVar("EnumType")


class ReportGenerator:
    """
    Converts and validates raw LLM JSON responses.
    """

    def generate(
        self,
        llm_response: str
    ) -> MarketIntelligenceReport:
        """
        Convert an LLM JSON response into a
        MarketIntelligenceReport.

        Parameters
        ----------
        llm_response : str
            Raw JSON string returned by the LLM.

        Returns
        -------
        MarketIntelligenceReport
            Typed market intelligence report.

        Raises
        ------
        ValueError
            If the JSON is invalid or required fields
            cannot be converted.
        """

        data = self._parse_json(llm_response)

        company = self._require_string(
            data,
            "company"
        )

        report_date = datetime.now()

        executive_summary = self._build_executive_summary(
            data.get("executive_summary", {})
        )

        events = self._build_events(
            company,
            data.get("events", [])
        )

        risks = self._build_risks(
            company,
            data.get("risks", [])
        )

        recommendations = self._build_recommendations(
            data.get("recommendations", [])
        )

        sources = self._build_sources(
            company,
            data.get("sources", [])
        )

        return MarketIntelligenceReport(
            company=company,
            report_date=report_date,
            executive_summary=executive_summary,
            events=events,
            risks=risks,
            recommendations=recommendations,
            sources=sources,
        )

# -------------------------------------------------------------
    @staticmethod
    def _parse_json(
        llm_response: str
    ) -> dict[str, Any]:
        """
        Parse JSON from an LLM response.

        Handles:
        - Plain JSON
        - Markdown JSON code fences
        - DeepSeek <think>...</think> blocks
        - Leading/trailing explanatory text
        """

        if not llm_response or not llm_response.strip():
            raise ValueError(
                "LLM returned an empty response."
            )

        text = llm_response.strip()

        # Remove DeepSeek reasoning block
        if "</think>" in text:
            text = text.split(
                "</think>",
                1
            )[1].strip()

        # Remove Markdown code fences
        if text.startswith("```"):

            if text.startswith("```json"):
                text = text[7:].strip()
            else:
                text = text[3:].strip()

            if text.endswith("```"):
                text = text[:-3].strip()

        # Find JSON object
        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end == -1 or end <= start:
            raise ValueError(
                "No JSON object found in LLM response."
            )

        json_text = text[start:end + 1]

        # Parse JSON
        try:
            data = json.loads(json_text)

        except json.JSONDecodeError as exc:

            print("JSON invalid. Trying repair...")

            try:
                fixed = repair_json(llm_response)

                data = json.loads(fixed)

                print("JSON repaired successfully.")

                return data

            except Exception as repair_exc:

                print("JSON repair failed.")

            print(fixed if 'fixed' in locals() else llm_response)

            raise ValueError(
                f"Invalid JSON returned by LLM.\n"
                f"Original Error : {exc}\n"
                f"Repair Error   : {repair_exc}"
            ) from repair_exc

        if not isinstance(data, dict):
            raise ValueError(
                "LLM response must be a JSON object."
            )

        return data

 # ------------------------------------------------------------------

    @staticmethod
    def _require_string(
        data: dict[str, Any],
        field_name: str
    ) -> str:
        """
        Return a required non-empty string.
        """

        value = data.get(field_name)

        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"Required field '{field_name}' is missing."
            )

        return value.strip()

    # ------------------------------------------------------------------

    @staticmethod
    def _parse_enum(
        enum_class: Type[EnumType],
        value: Any,
        field_name: str,
    ) -> EnumType | None:
        """
        Convert a string into an Enum value.
        Returns None for missing/empty values.
        """

    # Missing field
        if value is None:
            return None

    # Convert everything to string
        value = str(value).strip()

    # Empty string
        if value == "":
            return None

        for enum_value in enum_class:
            if value.lower() == enum_value.value.lower():
                return enum_value

        valid_values = [item.value for item in enum_class]

        raise ValueError(
            f"Invalid value '{value}' for '{field_name}'. "
            f"Valid values: {valid_values}"
       )

    # ------------------------------------------------------------------

    @staticmethod
    def _parse_datetime(
        value: Any,
        field_name: str,
    ) -> datetime | None:
        """
        Convert an ISO-8601 date/time string into datetime.
        
        Returns None when the LLM does not provide a date.
        """

        if value is None:
          return None

        if not isinstance(value, str):
          raise ValueError(
            f"Invalid datetime value for '{field_name}'."
        )

        value = value.strip()

        if not value:
          return None

        match = re.search(
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}",
        value,
        )
        if match:
          value = match.group(0)

        try:

           return datetime.fromisoformat(
            value.replace("Z", "+00:00")
            )

        except ValueError:

         #Invalid or unknown date
            return None

    # -------------------------------------------------------------------
    def _parse_confidence(
        self,
        value,
        field_name,
    ) -> float:

        if value in (None, ""):
            return 0.0

        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValueError(
                f"Field '{field_name}' must be a number."
            )

        if value < 0.0:
            return 0.0

        if value > 1.0:
            return 1.0

        return value   

    # ------------------------------------------------------------------
    # ------------------------------------------------------------------

    def _build_executive_summary(
        self,
        data: dict[str, Any]
    ) -> ExecutiveSummary:

        overview = data.get(
            "overview",
            ""
        )

        sentiment = self._parse_enum(
            Sentiment,
            data.get("sentiment", "Neutral"),
            "executive_summary.sentiment",
        )

        confidence = float(
            data.get("confidence", 0.0)
        )

        return ExecutiveSummary(
            overview=overview,
            sentiment=sentiment,
            confidence=confidence,
        )

    # ------------------------------------------------------------------

    def _build_events(
        self,
        company: str,
        events_data: list[Any]
    ) -> list[MarketEvent]:

        events: list[MarketEvent] = []

        for index, event in enumerate(
            events_data,
            start=1
        ):

            if not isinstance(event, dict):
                raise ValueError(
                    f"Event {index} is not a JSON object."
                )

            events.append(
                MarketEvent(
                    company=company,

                    title=event.get(
                        "title",
                        ""
                    ),

                    summary=event.get(
                        "summary",
                        ""
                    ),

                    event_type=self._parse_enum(
                        EventType,
                        event.get(
                            "event_type",
                            "Other"
                        ),
                        f"events[{index}].event_type",
                    ),

                    importance=self._parse_enum(
                        Importance,
                        event.get(
                            "importance",
                            "Medium"
                        ),
                        f"events[{index}].importance",
                    ),
                    business_impact=event.get(
                        "business_impact",
                        ""
                    ),

                    source=event.get(
                        "source",
                        ""
                    ),

                    url=event.get(
                        "url",
                        ""
                    ),

                    published=self._parse_datetime(
                        event.get("published"),
                        f"events[{index}].published",
                    ),

                    sentiment=self._parse_enum(
                        Sentiment,
                        event.get(
                            "sentiment",
                            "Neutral"
                        ),
                        f"events[{index}].sentiment",
                    ),

                    confidence=float(
                        event.get(
                            "confidence",
                            0.0
                        )
                    ),
                )
            )

        return events

    # ------------------------------------------------------------------

    def _build_risks(
        self,
        company: str,
        risks_data: list[Any]
    ) -> list[Risk]:

        risks: list[Risk] = []

        for index, risk in enumerate(
            risks_data,
            start=1
       ):

        # Skip completely empty or placeholder objects
            if not risk:
                continue

            if not risk.get("description", "").strip():
                continue

            risks.append(

                Risk(

                company=company,

                description=risk.get("description", "").strip(),
                 
                severity=self._parse_enum(
                    RiskSeverity,
                    risk.get("severity"),
                    f"risks[{index}].severity"
                ),

                impact=risk.get("impact", "").strip(),

                mitigation=risk.get("mitigation", "").strip(),

                confidence=self._parse_confidence(
                    risk.get("confidence"),
                    f"risks[{index}].confidence"
                )

            )

        )

        return risks


    # ------------------------------------------------------------------

   
    def _build_recommendations(
        self,
        recommendations_data: list[Any]
    ) -> list[Recommendation]:

        recommendations: list[Recommendation] = []

        for index, item in enumerate(
            recommendations_data,
            start=1
        ):

            # Skip empty entries
            if not item:
                continue

            # --------------------------------------------------
            # Case 1 : Recommendation returned as plain string
            # --------------------------------------------------
            if isinstance(item, str):

                text = item.strip()

                if not text:
                    continue

                recommendations.append(

                    Recommendation(

                        priority=Priority.MEDIUM,

                        recommendation=text,

                        rationale=""

                    )

                )

                continue

            # --------------------------------------------------
            # Case 2 : Recommendation returned as JSON object
            # --------------------------------------------------
            if isinstance(item, dict):

                recommendation = item.get(
                    "recommendation",
                    ""
                ).strip()

                if not recommendation:
                    continue

                recommendations.append(

                    Recommendation(

                        priority=self._parse_enum(
                            Priority,
                            item.get(
                                "priority",
                                "Medium"
                            ),
                            f"recommendations[{index}].priority",
                        ),

                        recommendation=recommendation,

                        rationale=item.get(
                            "rationale",
                            ""
                        ).strip(),

                    )

                )

                continue

            # --------------------------------------------------
            # Ignore unexpected types
            # --------------------------------------------------
            print(
                f"Skipping invalid recommendation type: {type(item)}"
            )

        return recommendations


    # ------------------------------------------------------------------

    def _build_sources(
        self,
        company: str,
        sources_data: list[Any]
    ) -> list[SourceArticle]:

        sources: list[SourceArticle] = []

        for index, source in enumerate(
            sources_data,
            start=1
        ):

            if not isinstance(source, dict):
                raise ValueError(
                    f"Source {index} is not a JSON object."
                )

            sources.append(
                SourceArticle(
                    company=company,

                    title=source.get(
                        "title",
                        ""
                    ),

                    source=source.get(
                        "source",
                        ""
                    ),

                    url=source.get(
                        "url",
                        ""
                    ),

                    published=self._parse_datetime(
                        source.get("published"),
                        f"sources[{index}].published",
                    ),

                    summary=source.get(
                        "summary",
                        ""
                    ),

                    keyword=source.get(
                        "keyword",
                        ""
                    ),
                )
            )

        return sources