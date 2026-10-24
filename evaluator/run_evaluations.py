import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

from evaluator.core import SUPPORTED, collect_submission, evaluate, load_problem
from evaluator.report_generator import write_reports

SUBMISSION_ROOTS = (
    "Submission-Milestone1",
    "Submission-Milestone2",
    "Submission-Milestone3",
    "Submission-Milestone4",
)

PROJECT_SIGNALS = {
    "Retail_Customer_Purchase": (
        "retail_purchase", "retail_customer_purchase", "customer purchase intelligence",
        "user_product_purchase_details", "customer_reviews"
    ),
    "Healthcare_Liver_Disease": (
        "healthcare", "liver_disease", "liver disease", "liver patient dataset",
        "healthcare_education_text"
    ),
    "Loan_Default": ("loan_default", "loan default", "default prediction", "credit risk")
}

def choose_project_milestone(path, config):
    path_text = path.as_posix().lower().replace("-", "_").replace(" ", "_")
    filename = path.stem.lower().replace("-", "_").replace(" ", "_")
    project_configs = config.get("projects", {})
    project = None

    # Prefer explicit project terms from filename/path.
    for project_name in project_configs:
        normalized = project_name.lower().replace("-", "_").replace(" ", "_")
        if normalized in path_text or normalized in filename:
            project = project_name
            break
    if project is None:
        for project_name, signals in PROJECT_SIGNALS.items():
            if project_name in project_configs and any(s.replace(" ", "_") in path_text or s.replace(" ", "_") in filename for s in signals):
                project = project_name
                break

    # Infer only from explicit project evidence inside text-based submissions.
    if project is None and path.suffix.lower() in {".ipynb", ".py", ".md", ".txt", ".json", ".html"}:
        try:
            sample = path.read_text(encoding="utf-8", errors="replace")[:50000].lower().replace("-", "_")
            for project_name, signals in PROJECT_SIGNALS.items():
                if project_name in project_configs and any(s.lower().replace(" ", "_") in sample for s in signals):
                    project = project_name
                    break
        except OSError:
            pass

    # Legacy submissions in submission/Participant_xxx belong to the configured default.
    if project is None and path.parts and path.parts[0].lower() == "submission":
        default = config.get("default_project", "Loan_Default")
        if default in project_configs:
            project = default
    if project is None:
        raise ValueError(
            f"Cannot identify project for {path}. Put the project name or a recognized project-specific keyword in the filename or notebook."
        )

    milestone_match = re.search(r"milestone[_ -]?([1-4])", path.as_posix(), re.IGNORECASE)
    if not milestone_match:
        milestone_match = re.search(r"_m([1-4])_", path.stem, re.IGNORECASE)
    if not milestone_match:
        raise ValueError(f"Cannot identify milestone from path {path}.")
    milestone = f"Milestone_{milestone_match.group(1)}"

    if milestone not in project_configs.get(project, {}).get("rubrics", {}):
        raise ValueError(f"No rubric configured for {project}/{milestone}.")
    return project, milestone

def supported_submission(path):
    return (
        path.is_file()
        and (path.suffix.lower() in SUPPORTED or path.suffix.lower() == ".zip")
        and not path.name.startswith(".")
        and path.name.lower() not in {"readme.md", "readme.txt", ".gitkeep"}
    )

def discover_submissions(files_from=None):
    found = set()
    for root_name in SUBMISSION_ROOTS:
        root = Path(root_name)
        if root.exists():
            found.update(p for p in root.rglob("*") if supported_submission(p))
    if files_from and Path(files_from).exists():
        for line in Path(files_from).read_text(encoding="utf-8").splitlines():
            p = Path(line.strip())
            if p.exists() and supported_submission(p):
                found.add(p)
    return sorted(found, key=lambda p: p.as_posix().lower())

def participant_name(path):
    p = Path(path)
    match = re.search(r"(Participant(?:[_ -]M[1-4])?[_ -]*\d+)", p.stem, re.IGNORECASE)
    if match:
        return re.sub(r"[ -]+", "_", match.group(1)).replace("__", "_")
    match = re.search(r"(Participant[_ -]*\d+)", p.as_posix(), re.IGNORECASE)
    return re.sub(r"[ -]+", "_", match.group(1)).replace("__", "_") if match else p.stem

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--files-from", required=False, default="all_submissions.txt")
    parser.add_argument("--output-dir", default="evaluation-reports")
    args = parser.parse_args()

    config = json.loads(Path("evaluator/config.json").read_text(encoding="utf-8"))
    candidates = discover_submissions(args.files_from)
    if not candidates:
        print("No supported submission files found in the four milestone folders.")
        return 0
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY secret is missing.", file=sys.stderr)
        return 2

    # Every run regenerates complete report workbooks from all submissions, not just changed files.
    output_dir = Path(args.output_dir)
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    completed, failed = 0, 0
    for path in candidates:
        try:
            project, milestone = choose_project_milestone(path, config)
            project_config = config["projects"][project]
            rubric_path = project_config.get("rubrics", {}).get(milestone)
            if not rubric_path or not Path(rubric_path).exists():
                raise FileNotFoundError(f"Configured rubric does not exist: {rubric_path}")
            rubric = json.loads(Path(rubric_path).read_text(encoding="utf-8"))
            if not rubric.get("criteria"):
                raise ValueError(f"Rubric has no criteria: {rubric_path}")
            problem_path = project_config.get("problem_statement")
            if not problem_path or not Path(problem_path).exists():
                raise FileNotFoundError(f"Configured problem statement does not exist: {problem_path}")
            problem = load_problem(problem_path)
            evidence, included = collect_submission(
                [path],
                int(config.get("max_file_chars", 18000)),
                int(config.get("max_total_chars", 45000)),
            )
            if not evidence.strip():
                raise ValueError("No readable text extracted from submission.")
            result = evaluate(evidence, rubric, problem, config.get("model", "gpt-4.1-mini"))
            result["project_id"] = project
            result["milestone_id"] = milestone
            report_path, _ = write_reports(result, path.as_posix(), output_dir)
            completed += 1
            print(f"Evaluated {path}: {result.get('total_marks', 0)}/{result.get('maximum_marks', 100)} | {report_path}")
        except Exception as exc:
            failed += 1
            print(f"ERROR evaluating {path}: {type(exc).__name__}: {exc}", file=sys.stderr)

    print(f"Finished evaluations: {completed} successful; {failed} failed.")
    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())
