# AI_Evaluator: Multi-project setup

This repository supports three project domains across four milestones:
- Loan Default Prediction and Risk Intelligence
- Retail Customer Purchase Behaviour Prediction
- Liver Disease Prediction & AI-Powered Decision Support

Retail Sales Forecasting files have been removed.

## Submission folders
- `Submission-Milestone1/`
- `Submission-Milestone2/`
- `Submission-Milestone3/`
- `Submission-Milestone4/`

Each folder can contain submissions from any of the three supported domains. Include one of these project keywords in the notebook filename: `loan_default`, `retail_purchase`, or `healthcare`.

## Evaluation
The workflow scans all tracked notebooks in the four milestone folders on every manual run, selects the corresponding problem statement and milestone rubric, and produces one consolidated Excel report for each milestone. Reports are uploaded in the `evaluation-reports-<run number>` artifact.

## Setup
1. Ensure the `OPENAI_API_KEY` repository secret exists.
2. Upload submissions into the correct milestone folder.
3. Go to **Actions → Evaluate Participant Submissions → Run workflow**.
4. Download the artifact after the run completes.

The evaluator reads submissions and does not execute untrusted participant code. Scores and feedback need human review.
