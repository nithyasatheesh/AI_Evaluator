# Project: Loan Default Prediction and Risk Intelligence

## Business context
Analyze loan applications and repayment/default outcomes to understand patterns associated with default, build predictive baselines, compare machine-learning and deep-learning approaches, and communicate findings with responsible AI safeguards.

## Data and assumptions
Use the loan-default dataset supplied with this project. Inspect actual filenames, columns, target encoding, missingness, duplicates, identifier fields and target balance before modeling. Do not invent unprovided columns or assume undocumented target codes.

## Milestone 1 — Data understanding and baseline
Profile the dataset, conduct EDA, clean and engineer features, establish a logistic-regression baseline, and report confusion matrix, precision, recall, F1 and ROC-AUC where appropriate.

## Milestone 2 — Machine learning
Develop and compare suitable classifiers, tune hyperparameters using training-only cross-validation, analyze feature importance cautiously, and explore borrower segments with clustering where appropriate.

## Milestone 3 — Deep learning and NLP
Implement a neural network for the verified default target, compare it with a selected ML model on the same held-out data, assess overfitting, and perform a defined NLP task using relevant text if such data is supplied.

## Milestone 4 — Generative AI and agentic workflows
Build evidence-grounded LLM explanations, RAG over approved policy/reference documents, safe read-only Text-to-SQL, and agent/tool orchestration. Evaluate factual grounding, safety, privacy, fairness, prompt-injection resistance and limitations.

## Expected evidence
Provide notebooks/source, quality checks, plots, preprocessing decisions, model metrics, comparisons, interpretations, validation evidence and limitations. Score only evidence present in the submission. Never claim code was executed when it was not.

## Responsible use
Do not invent metrics or feature meanings, do not treat correlation as causation, and do not use model output as the sole basis for credit decisions. Protect applicant information and require human oversight.
