
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


def export_bug_report(bug_report, filename="AI_Generated_Bug_Report.xlsx"):

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Bug Report"

    headers = [
        "Bug Title",
        "Description",
        "Steps to Reproduce",
        "Expected Result",
        "Actual Result",
        "Severity",
        "Priority",
        "Probable Root Cause",
        "Suggested Fix"
    ]

    values = [
        bug_report["bug_title"],
        bug_report["description"],
        "\n".join(
            bug_report["steps_to_reproduce"]
        ),
        bug_report["expected_result"],
        bug_report["actual_result"],
        bug_report["severity"],
        bug_report["priority"],
        bug_report["root_cause"],
        bug_report["suggested_fix"]
    ]

    # Add headers
    for col, header in enumerate(headers, start=1):

        cell = sheet.cell(row=1, column=col)
        cell.value = header
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(
            start_color="1F4E78",
            end_color="1F4E78",
            fill_type="solid"
        )
        cell.alignment = Alignment(
            horizontal="center",
            vertical="center",
            wrap_text=True
        )

    # Add bug report data
    for col, value in enumerate(values, start=1):

        cell = sheet.cell(row=2, column=col)
        cell.value = value
        cell.alignment = Alignment(
            vertical="top",
            wrap_text=True
        )

    # Column widths
    column_widths = [
        35, 45, 50, 40, 40, 15, 15, 45, 45
    ]

    for index, width in enumerate(column_widths, start=1):
        sheet.column_dimensions[
            get_column_letter(index)
        ].width = width

    # Row height
    sheet.row_dimensions[1].height = 30
    sheet.row_dimensions[2].height = 120

    # Borders
    thin_border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin")
    )

    for row in sheet.iter_rows(
        min_row=1,
        max_row=2,
        min_col=1,
        max_col=len(headers)
    ):
        for cell in row:
            cell.border = thin_border

    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = "A1:I2"

    workbook.save(filename)

    print(f"\nExcel report generated: {filename}")
