"""Generate one consolidated Excel report per milestone."""
import re
from pathlib import Path

import pandas as pd
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

MILESTONE_CRITERIA = {
    "Milestone_1": [
        ("Data Understanding & Quality Checks", 20),
        ("Exploratory Data Analysis (EDA)", 20),
        ("Data Cleaning & Feature Engineering", 20),
        ("Logistic Regression Baseline", 20),
        ("Evaluation & Findings", 20),
    ],
    "Milestone_2": [
        ("ML Model Development", 25),
        ("Hyperparameter Tuning & Validation", 20),
        ("Model Comparison & Performance Evaluation", 20),
        ("Risk Factor / Feature Importance Analysis", 15),
        ("Clustering & Borrower Segmentation", 20),
    ],
    "Milestone_3": [
        ("Neural Network Design & Implementation", 25),
        ("Data Preparation & Training", 20),
        ("Model Evaluation & Overfitting Analysis", 20),
        ("ML vs DL Comparison", 15),
        ("NLP Implementation & Findings", 20),
    ],
    "Milestone_4": [
        ("LLM Explanations & Prompt Engineering", 20),
        ("RAG: Ingestion/Retrieval/Grounding", 20),
        ("Text-to-SQL & Query Safety", 20),
        ("AI Agent Orchestration", 20),
        ("Evaluation & Responsible AI", 20),
    ],
}
BASE_COLUMNS = ["Participant Name", "Submission File", "Project", "Milestone"]
SCORE_COLUMNS = ["Total Score", "Maximum Score"]
FEEDBACK_COLUMNS = ["Area of Strength", "Area for Improvement", "Overall Feedback"]


def _participant_name(source_file: str) -> str:
    path = Path(source_file)
    for item in [path.stem, *reversed(path.parts[:-1])]:
        match = re.search(r"(participant[_ -]*\\d+)", item, re.IGNORECASE)
        if match:
            return re.sub(r"[\\s-]+", "_", match.group(1)).replace("__", "_")
    return path.parent.name or path.stem


def _feedback_text(value):
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        return "\\n".join(str(item) for item in value if item is not None)
    return str(value)


def _format_worksheet(ws):
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="1F4E78")
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    for column_cells in ws.columns:
        letter = get_column_letter(column_cells[0].column)
        header = str(column_cells[0].value or "")
        max_len = max((len(str(c.value or "")) for c in column_cells), default=12)
        if header in FEEDBACK_COLUMNS:
            width = 48
        elif header == "Submission File":
            width = 48
        else:
            width = min(38, max(12, max_len + 2))
        ws.column_dimensions[letter].width = width
        for cell in column_cells:
            cell.alignment = Alignment(wrap_text=True, vertical="top")


def _milestone_row(result, source_file):
    milestone = str(result.get("milestone_id", "Milestone_1"))
    criteria = MILESTONE_CRITERIA.get(milestone, [])
    columns = BASE_COLUMNS + [
        f"{name} ({max_marks})" for name, max_marks in criteria
    ] + SCORE_COLUMNS + FEEDBACK_COLUMNS
    row = {column: "" for column in columns}
    row.update({
        "Participant Name": _participant_name(source_file),
        "Submission File": str(source_file).replace("\\\\", "/"),
        "Project": result.get("project_id", "Loan_Default"),
        "Milestone": milestone,
        "Total Score": result.get("total_marks", 0),
        "Maximum Score": result.get("maximum_marks", sum(m for _, m in criteria)),
        "Area of Strength": _feedback_text(result.get("strengths", [])),
        "Area for Improvement": _feedback_text(result.get("areas_for_improvement", [])),
        "Overall Feedback": _feedback_text(result.get("overall_feedback", "")),
    })
    scores = {
        str(c.get("name", "")).strip().casefold(): c.get("marks_awarded", "")
        for c in result.get("criteria", [])
    }
    for name, max_marks in criteria:
        row[f"{name} ({max_marks})"] = scores.get(name.casefold(), "")
    return columns, row


def write_reports(result, source_file, output_dir):
    """Append this submission to the single Excel workbook for its milestone."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    milestone = str(result.get("milestone_id", "Milestone_1"))
    milestone_number = milestone.rsplit("_", 1)[-1]
    report_folder = out / f"Submission-Milestone{milestone_number}-Report"
    report_folder.mkdir(parents=True, exist_ok=True)
    report_path = report_folder / f"Submission-Milestone{milestone_number}-Report.xlsx"

    columns, new_row = _milestone_row(result, source_file)
    rows = []
    if report_path.exists():
        try:
            existing = pd.read_excel(report_path, sheet_name="Feedback Report").fillna("")
            rows = existing.to_dict(orient="records")
        except (ValueError, OSError, ImportError):
            rows = []

    # Replace an existing row for the same submission if the workflow is rerun.
    key = (str(new_row["Submission File"]), str(new_row["Milestone"]))
    rows = [
        row for row in rows
        if (str(row.get("Submission File", "")), str(row.get("Milestone", ""))) != key
    ]
    rows.append(new_row)
    frame = pd.DataFrame(rows).reindex(columns=columns).fillna("")
    frame = frame.drop_duplicates(subset=["Submission File", "Milestone"], keep="last")
    frame = frame.sort_values(["Participant Name", "Submission File"], kind="stable")

    with pd.ExcelWriter(report_path, engine="openpyxl") as writer:
        frame.to_excel(writer, index=False, sheet_name="Feedback Report")
        _format_worksheet(writer.book["Feedback Report"])

    return report_path, None
