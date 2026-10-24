# AI_Evaluator

AI-powered rubric-based evaluation of project submissions across four milestones.

## Supported project domains
- **Loan Default Prediction and Risk Intelligence**
- **Retail Customer Purchase Behaviour Prediction**
- **Liver Disease Prediction & AI-Powered Decision Support**

Retail Sales Forecasting has been removed from this repository's supported projects.

## Reports
Each workflow run uploads an `evaluation-reports-<run number>` artifact containing one consolidated Excel report per milestone:
- `Submission-Milestone1-Report/Submission-Milestone1-Report.xlsx`
- `Submission-Milestone2-Report/Submission-Milestone2-Report.xlsx`
- `Submission-Milestone3-Report/Submission-Milestone3-Report.xlsx`
- `Submission-Milestone4-Report/Submission-Milestone4-Report.xlsx`

Reports combine all evaluated project domains for that milestone. Criterion columns not relevant to a project's rubric remain blank.

## Setup
1. Store `OPENAI_API_KEY` as a GitHub Actions repository secret.
2. Upload notebooks into the appropriate `Submission-MilestoneN/` folder. Include `loan_default`, `retail_purchase`, or `healthcare` in each notebook filename.
3. Go to **Actions → Evaluate Participant Submissions → Run workflow**.
4. Download the evaluation report artifact.

The evaluator reads submissions as evidence; it does not execute participant notebooks or source code. AI-generated scores require human review before being treated as final grades.
