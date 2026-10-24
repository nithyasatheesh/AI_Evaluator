# Project: Liver Disease Prediction & AI-Powered Decision Support

## Goal
Use patient demographic and clinical measurements to explore patterns associated with liver disease and compare predictive models as an educational decision-support exercise.

## Data sources
Use the supplied project files where available: Liver Patient Dataset.csv, Status.xlsx, Cityname_statecode.xlsx, Statecode_name.xlsx, Healthcare_Education_Text.csv, Liver_Health_Education_Guide.pdf and Healthcare_AI_Responsible_Use_Guide.pdf. Inspect schemas and confirm identifiers and target coding before joining. The stated Status mapping is 1 = Liver Patient and 2 = Non-Liver Patient; verify against the supplied files. Exclude identifiers from model features.

## Milestone 1 — EDA and baseline modelling
Profile data quality and target balance, analyze age/gender/clinical measurements, decode lookup values where appropriate, handle missingness and outliers with justification, engineer features, build a Logistic Regression baseline, and evaluate with confusion matrix, precision, recall, F1 and ROC-AUC where valid.

## Milestone 2 — Machine learning
Develop and compare Decision Tree, Random Forest and boosting classifiers. Use stratified validation and training-only tuning, inspect false negatives and class-sensitive metrics, explain feature importance cautiously, and label any predicted-probability risk bands as illustrative rather than clinically validated.

## Milestone 3 — Deep learning and NLP
Build a neural-network classifier, compare it with the best ML model on the same held-out data, assess overfitting, and complete a defined NLP task using the supplied healthcare education text.

## Milestone 4 — Generative AI and agents
Use grounded prompts, RAG over approved healthcare education documents with source citations, validated read-only SQL, and separate tools for queries, retrieval and summarization. Evaluate factual grounding, privacy, fairness, prompt injection, uncertainty and escalation of clinical questions.

## Expected evidence
Data checks, target mapping, EDA plots, leakage-aware preprocessing, model metrics, comparison tables, interpretation, NLP evidence, source-grounded responses and limitations.

## Safety constraints
This is educational work and is not a medical device. Never present the model as a diagnosis or source of treatment advice. Protect patient information, discuss false negatives and bias, distinguish associations from causes, and require qualified clinical review for clinical decisions. Do not invent metrics or claim code was executed.
