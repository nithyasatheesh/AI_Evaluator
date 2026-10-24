# Updated milestone submission folders and workflow files

This package is designed for the repository `nithyasatheesh/Project-Case-Study-Evaluations`. It includes one sample notebook per milestone, updated milestone rubrics, and workflow/script changes for the folder naming convention.

## Folder names
- `Submission-Milestone1/`
- `Submission-Milestone2/`
- `Submission-Milestone3/`
- `Submission-Milestone4/`

Each sample notebook is synthetic/demo material only. Replace it with the actual participant submission before grading.

## Files to replace in GitHub
Upload/replace these files at the same paths in your repository:
1. `.github/workflows/evaluate-submissions.yml`
2. `scripts/find_submissions.py`
3. `evaluator/run_evaluations.py`
4. `rubrics/Loan_Default/milestone_1_rubric.json` through `milestone_4_rubric.json`

Then upload each sample notebook to its matching `Submission-MilestoneN/` folder. Do not upload the entire ZIP as a single file into the repository; extract it locally first and upload the individual files/folders, preserving their paths.

## Test workflow
- Ensure GitHub repository secret `OPENAI_API_KEY` exists.
- Commit the updated workflow/script/rubric files.
- Go to Actions → Evaluate Participant Submissions → Run workflow. Manual dispatch scans all existing supported files in all four milestone folders.
- Check both `Evaluate submissions` and `Upload evaluation reports` steps. Download the report artifact.
- Later participant uploads under one of the four folders trigger the workflow on push.

## Important limitations
- GitHub Actions success does not mean a score was produced: inspect logs and the uploaded artifact.
- The sample notebooks use toy/synthetic data and are only for testing the pipeline.
- The workflow evaluates the changed files individually; it does not yet merge all participants/milestones into a single consolidated Excel workbook. The included report generator produces reports per evaluated submission. If you require one master workbook with one row per participant per milestone, that needs an additional consolidation step.
- Do not execute submitted Python/notebook code in GitHub Actions. The evaluator reads the submission content for rubric-based review; it does not need to run untrusted student code.
- For real learner work, use a private repository and least-privilege access.
