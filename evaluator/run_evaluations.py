import argparse
import json
import os
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


def choose_project_milestone(path, config):
    lower_parts = [part.lower().replace("-", "_") for part in path.parts]
    milestone = next(
        (
            f"Milestone_{i}"
            for i in range(1, 5)
            if f"submission_milestone{i}" in lower_parts
            or f"milestone_{i}" in lower_parts
            or f"milestone{i}" in path.as_posix().lower()
        ),
        None,
    )
    project = config.get("default_project", "Loan_Default")
    projects = config.get("projects", {})
    for configured_project in projects:
        if configured_project.lower() in lower_parts:
            project = configured_project
            break
    project_config = projects.get(project, {})
    if milestone not in project_config.get("rubrics", {}):
        milestone = config.get("default_milestone", "Milestone_1")
    return project, milestone


def supported_submission(path):
    return (
        path.is_file()
        and path.suffix.lower() in (set(SUPPORTED) | {".zip"})
        and not path.name.startswith(".")
        and path.name.lower() not in {"readme.md", "readme.txt"}
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--files-from", required=True)
    parser.add_argument("--output-dir", default="evaluation-reports")
    args = parser.parse_args()

    config = json.loads(Path("evaluator/config.json").read_text(encoding="utf-8"))
    listed_paths = [
        Path(line.strip())
        for line in Path(args.files_from).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    # Rebuild the consolidated workbook from all current submissions on every run.
    # This is necessary because GitHub-hosted runners start with a clean workspace.
    all_paths = set(listed_paths)
    for root_name in SUBMISSION_ROOTS:
        root = Path(root_name)
        if root.exists():
            all_paths.update(p for p in root.rglob("*") if supported_submission(p))

    allowed_roots = {name.lower() for name in SUBMISSION_ROOTS}
    candidates = sorted(
        (
            path for path in all_paths
            if path.exists()
            and supported_submission(path)
            and path.parts
            and path.parts[0].lower() in allowed_roots
        ),
        key=lambda path: path.as_posix().lower(),
    )

    if not candidates:
        print("No supported submission files found.")
        return 0
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY secret is missing.", file=sys.stderr)
        return 2

    output_dir = Path(args.output_dir)
    # A clean report directory ensures the master workbook only includes this run's
    # complete set of submissions rather than stale rows from an earlier run.
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    completed = 0
    for path in candidates:
        project, milestone = choose_project_milestone(path, config)
        project_config = config.get("projects", {}).get(project, {})
        rubric_path = project_config.get("rubrics", {}).get(milestone)
        if not rubric_path or not Path(rubric_path).exists():
            print(f"Skipping {path}: rubric not configured for {project}/{milestone}.")
            continue
        rubric = json.loads(Path(rubric_path).read_text(encoding="utf-8"))
        if not rubric.get("criteria"):
            print(f"Skipping {path}: rubric {milestone} has no criteria.")
            continue
        problem = load_problem(project_config.get("problem_statement"))
        evidence, included = collect_submission(
            [path],
            int(config.get("max_file_chars", 18000)),
            int(config.get("max_total_chars", 45000)),
        )
        if not evidence.strip():
            print(f"Skipping {path}: no text extracted.")
            continue
        result = evaluate(evidence, rubric, problem, config.get("model", "gpt-4.1-mini"))
        xlsx, js = write_reports(result, path.as_posix(), output_dir)
        completed += 1
        print(f"{path}: {result['total_marks']}/{result['maximum_marks']} | milestone report: {xlsx}")

    print(f"Evaluated {completed} submission(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
