"""
excel_writer.py

Converts a MarketIntelligenceReport into a formatted
Excel workbook using XlsxWriter.

Author : Madhu
Version : 1.0
"""

from pathlib import Path

import xlsxwriter
from datetime import datetime
from models.models import MarketIntelligenceReport


class ExcelWriter:
    """
    Writes Market Intelligence reports to Excel.
    """

    def __init__(
        self,
        output_directory: str = "reports",
    ) -> None:

        self.output_directory = Path(
            output_directory
        )

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True
        )

    # ------------------------------------------------------------------

    def write(
        self,
        report: MarketIntelligenceReport,
        filename: str | None = None,
    ) -> Path:
        """
        Write a MarketIntelligenceReport to Excel.

        Parameters
        ----------
        report:
            Market intelligence report.

        filename:
            Optional workbook filename.

        Returns
        -------
        Path
            Generated workbook path.
        """

        if filename is None:
            filename = (
                f"{self._safe_name(report.company)}"
                "_Market_Intelligence_Report.xlsx"
            )

        output_path = (
            self.output_directory / filename
        )

        workbook = xlsxwriter.Workbook(
            str(output_path),
            { "remove_timezone": True}
        )

        try:
            self._write_summary(
                workbook,
                report
            )

            self._write_events(
                workbook,
                report
            )

            self._write_risks(
                workbook,
                report
            )

            self._write_recommendations(
                workbook,
                report
            )

            self._write_sources(
                workbook,
                report
            )

        finally:
            workbook.close()

        return output_path

    # ------------------------------------------------------------------

    def _create_formats(
        self,
        workbook,
    ):
        """Create reusable workbook formats."""

        return {
            "title": workbook.add_format({
                "bold": True,
                "font_size": 16,
                "font_color": "white",
                "bg_color": "#1F4E78",
                "align": "center",
                "valign": "vcenter",
            }),

            "header": workbook.add_format({
                "bold": True,
                "font_color": "white",
                "bg_color": "#4472C4",
                "border": 1,
                "align": "center",
                "valign": "vcenter",
                "text_wrap": True,
            }),

            "label": workbook.add_format({
                "bold": True,
                "bg_color": "#D9EAF7",
                "border": 1,
            }),

            "text": workbook.add_format({
                "border": 1,
                "text_wrap": True,
                "valign": "top",
            }),

            "date": workbook.add_format({
                "border": 1,
                "num_format": "yyyy-mm-dd hh:mm",
                "valign": "top",
            }),

            "number": workbook.add_format({
                "border": 1,
                "num_format": "0.00",
                "valign": "top",
            }),

            "url": workbook.add_format({
                "border": 1,
                "font_color": "0563C1",
                "underline": 1,
                "text_wrap": True,
            }),

            "critical": workbook.add_format({
                "bg_color": "#F4CCCC",
                "font_color": "#9C0006",
                "border": 1,
                "text_wrap": True,
            }),

            "high": workbook.add_format({
                "bg_color": "#FCE5CD",
                "font_color": "#C65911",
                "border": 1,
                "text_wrap": True,
            }),
        }

    # ------------------------------------------------------------------

    @staticmethod
    def _excel_datetime(value: datetime) -> datetime:
        """
        Convert a timezone-aware datetime into a naive datetime
    suitable for Excel.
        """
        if value.tzinfo is not None:
            return value.astimezone().replace(tzinfo=None)
        return value



    def _write_summary(
        self,
        workbook,
        report: MarketIntelligenceReport,
    ) -> None:

        worksheet = workbook.add_worksheet(
            "Executive Summary"
        )

        formats = self._create_formats(
            workbook
        )

        worksheet.merge_range(
            "A1:F1",
            f"Market Intelligence Report - "
            f"{report.company}",
            formats["title"],
        )

        worksheet.set_row(
            0,
            28
        )

        summary = report.executive_summary

        rows = [
            ("Company", report.company),
            ("Report Date", report.report_date),
            (
                "Sentiment",
                summary.sentiment.value
            ),
            (
                "Confidence",
                summary.confidence
            ),
            (
                "Executive Summary",
                summary.overview
            ),
            (
                "Major Events",
                len(report.events)
            ),
            (
                "Risks",
                len(report.risks)
            ),
            (
                "Recommendations",
                len(report.recommendations)
            ),
            (
                "Sources",
                len(report.sources)
            ),
        ]

        for row, (label, value) in enumerate(
            rows,
            start=2
        ):

            worksheet.write(
                row,
                0,
                label,
                formats["label"]
            )

            if label == "Report Date":

                worksheet.write_datetime(
                    row,
                    1,
                    self._excel_datetime(value),
                    formats["date"]
                )

            elif label == "Confidence":

                worksheet.write_number(
                    row,
                    1,
                    float(value),
                    formats["number"]
                )

            else:

                worksheet.write(
                    row,
                    1,
                    value,
                    formats["text"]
                )

        worksheet.set_column(
            "A:A",
            24
        )

        worksheet.set_column(
            "B:B",
            65
        )

        worksheet.freeze_panes(
            2,
            0
        )

    # ------------------------------------------------------------------

    def _write_events(
        self,
        workbook,
        report: MarketIntelligenceReport,
    ) -> None:

        worksheet = workbook.add_worksheet(
            "Events"
        )

        formats = self._create_formats(
            workbook
        )

        headers = [
            "Company",
            "Title",
            "Event Type",
            "Importance",
            "Summary",
            "Business Impact",
            "Sentiment",
            "Confidence",
            "Source",
            "Published",
            "URL",
        ]

        worksheet.write_row(
            0,
            0,
            headers,
            formats["header"]
        )

        for row, event in enumerate(
            report.events,
            start=1
        ):

            worksheet.write(
                row,
                0,
                event.company,
                formats["text"]
            )

            worksheet.write(
                row,
                1,
                event.title,
                formats["text"]
            )

            worksheet.write(
                row,
                2,
                event.event_type.value,
                formats["text"]
            )

            importance_format = formats["text"]

            if event.importance.value == "Critical":
                importance_format = formats["critical"]

            elif event.importance.value == "High":
                importance_format = formats["high"]

            worksheet.write(
                row,
                3,
                event.importance.value,
                importance_format
            )

            worksheet.write(
                row,
                4,
                event.summary,
                formats["text"]
            )

            worksheet.write(
                row,
                5,
                event.business_impact,
                formats["text"]
            )

            worksheet.write(
                row,
                6,
                event.sentiment.value,
                formats["text"]
            )

            worksheet.write_number(
                row,
                7,
                event.confidence,
                formats["number"]
            )

            worksheet.write(
                row,
                8,
                event.source,
                formats["text"]
            )
        if event.published is not None:
            worksheet.write_datetime(
                row,
                9,
                self._excel_datetime(event.published),
                formats["date"]
            )
        else:

            worksheet.write(
                row,
                9,
                 "",
                formats["text"]
                )


            if event.url:

                worksheet.write_url(
                    row,
                    10,
                    event.url,
                    formats["url"],
                    event.url
                )

            else:

                worksheet.write(
                    row,
                    10,
                    "",
                    formats["text"]
                )

        if report.events:

            last_row = len(report.events)

            worksheet.autofilter(
                0,
                0,
                last_row,
                len(headers) - 1
            )

            worksheet.freeze_panes(
                1,
                0
            )

        widths = [
            18,
            42,
            20,
            14,
            50,
            50,
            14,
            12,
            20,
            20,
            55,
        ]

        for column, width in enumerate(
            widths
        ):

            worksheet.set_column(
                column,
                column,
                width
            )

    # ------------------------------------------------------------------

    def _write_risks(
        self,
        workbook,
        report: MarketIntelligenceReport,
    ) -> None:

        worksheet = workbook.add_worksheet(
            "Risks"
        )

        formats = self._create_formats(
            workbook
        )

        headers = [
            "Company",
            "Description",
            "Severity",
            "Impact",
            "Mitigation",
            "Confidence",
        ]

        worksheet.write_row(
            0,
            0,
            headers,
            formats["header"]
        )

        for row, risk in enumerate(
            report.risks,
            start=1
        ):

            worksheet.write(
                row,
                0,
                risk.company,
                formats["text"]
            )

            worksheet.write(
                row,
                1,
                risk.description,
                formats["text"]
            )

            severity_format = formats["text"]

            if risk.severity.value == "Critical":
                severity_format = formats["critical"]

            elif risk.severity.value == "High":
                severity_format = formats["high"]

            worksheet.write(
                row,
                2,
                risk.severity.value,
                severity_format
            )

            worksheet.write(
                row,
                3,
                risk.impact,
                formats["text"]
            )

            worksheet.write(
                row,
                4,
                risk.mitigation,
                formats["text"]
            )

            worksheet.write_number(
                row,
                5,
                risk.confidence,
                formats["number"]
            )

        if report.risks:

            last_row = len(report.risks)

            worksheet.autofilter(
                0,
                0,
                last_row,
                len(headers) - 1
            )

            worksheet.freeze_panes(
                1,
                0
            )

        worksheet.set_column(
            "A:A",
            18
        )

        worksheet.set_column(
            "B:B",
            55
        )

        worksheet.set_column(
            "C:C",
            14
        )

        worksheet.set_column(
            "D:E",
            50
        )

        worksheet.set_column(
            "F:F",
            12
        )

    # ------------------------------------------------------------------

    def _write_recommendations(
        self,
        workbook,
        report: MarketIntelligenceReport,
    ) -> None:

        worksheet = workbook.add_worksheet(
            "Recommendations"
        )

        formats = self._create_formats(
            workbook
        )

        headers = [
            "Priority",
            "Recommendation",
            "Rationale",
        ]

        worksheet.write_row(
            0,
            0,
            headers,
            formats["header"]
        )

        for row, recommendation in enumerate(
            report.recommendations,
            start=1
        ):

            worksheet.write(
                row,
                0,
                recommendation.priority.value,
                formats["text"]
            )

            worksheet.write(
                row,
                1,
                recommendation.recommendation,
                formats["text"]
            )

            worksheet.write(
                row,
                2,
                recommendation.rationale,
                formats["text"]
            )

        if report.recommendations:

            last_row = len(
                report.recommendations
            )

            worksheet.autofilter(
                0,
                0,
                last_row,
                2
            )

            worksheet.freeze_panes(
                1,
                0
            )

        worksheet.set_column(
            "A:A",
            15
        )

        worksheet.set_column(
            "B:B",
            55
        )

        worksheet.set_column(
            "C:C",
            55
        )

    # ------------------------------------------------------------------

    def _write_sources(
        self,
        workbook,
        report: MarketIntelligenceReport,
    ) -> None:

        worksheet = workbook.add_worksheet(
            "Sources"
        )

        formats = self._create_formats(
            workbook
        )

        headers = [
            "Company",
            "Title",
            "Source",
            "Published",
            "Keyword",
            "URL",
            "Summary",
        ]

        worksheet.write_row(
            0,
            0,
            headers,
            formats["header"]
        )

        for row, source in enumerate(
            report.sources,
            start=1
        ):

            worksheet.write(
                row,
                0,
                source.company,
                formats["text"]
            )

            worksheet.write(
                row,
                1,
                source.title,
                formats["text"]
            )

            worksheet.write(
                row,
                2,
                source.source,
                formats["text"]
            )


            if source.published is not None: 

               worksheet.write_datetime(
                row,
                3,
                self._excel_datetime(source.published),
                formats["date"]
                )
            else:
                worksheet.write(
                    row,
                    3,
                    "",
                    formats["text"]
                )

            worksheet.write(
                row,
                4,
                source.keyword,
                formats["text"]
            )

            if source.url:

                worksheet.write_url(
                    row,
                    5,
                    source.url,
                    formats["url"],
                    source.url
                )

            else:

                worksheet.write(
                    row,
                    5,
                    "",
                    formats["text"]
                )

            worksheet.write(
                row,
                6,
                source.summary,
                formats["text"]
            )

        if report.sources:

            last_row = len(report.sources)

            worksheet.autofilter(
                0,
                0,
                last_row,
                len(headers) - 1
            )

            worksheet.freeze_panes(
                1,
                0
            )

        worksheet.set_column(
            "A:A",
            18
        )

        worksheet.set_column(
            "B:B",
            45
        )

        worksheet.set_column(
            "C:C",
            20
        )

        worksheet.set_column(
            "D:D",
            20
        )

        worksheet.set_column(
            "E:E",
            18
        )

        worksheet.set_column(
            "F:F",
            55
        )

        worksheet.set_column(
            "G:G",
            55
        )

    # ------------------------------------------------------------------

    @staticmethod
    def _safe_name(
        name: str
    ) -> str:
        """
        Make a company name safe for use as a filename.
        """

        invalid_characters = (
            '<>:"/\\|?*'
        )

        result = name

        for character in invalid_characters:
            result = result.replace(
                character,
                "_"
            )

        return result.strip()