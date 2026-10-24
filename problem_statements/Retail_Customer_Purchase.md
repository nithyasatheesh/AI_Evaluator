# Project: Retail Customer Purchase Behaviour Prediction & AI-Powered Intelligence

## Goal
Predict customer purchase amount, understand purchasing patterns, identify customer-value segments, and generate evidence-based insights for marketing and inventory planning.

## Data sources
Use the project datasets if supplied: user_demographics.csv, User_product_purchase_details.csv, Customer_Reviews.csv, product information and promotion/discount policy reference documents. Inspect actual schemas, join keys, data types and missingness before using the data. Do not invent columns or results.

## Milestone 1 — EDA and baseline modelling
Join demographic and purchase records using the verified customer key, check join cardinality and data quality, explore target and category patterns, clean data, engineer features, build a Linear Regression baseline for Purchase, and report MAE, RMSE and R².

## Milestone 2 — Machine learning
Develop and compare Decision Tree, Random Forest and boosting regression models. Tune on training/validation data, compare using consistent MAE/RMSE/R², interpret feature importance without implying causation, and cluster customers using aggregated purchase behaviour.

## Milestone 3 — Deep learning and NLP
Build a neural-network regression model for purchase amount, compare it to the best ML model on the same holdout, and perform a clearly defined NLP task on customer reviews. Do not fabricate labels or model metrics when the text data does not support them.

## Milestone 4 — Generative AI and agents
Generate explanations only from validated analysis results; implement RAG over approved product/promotion reference documents with citations; provide schema-constrained read-only Text-to-SQL; coordinate retrieval, data analysis and summarization tools; and evaluate grounding, SQL safety, privacy, prompt injection and unsupported claims.

## Expected evidence
Notebook/code, data checks, plots and interpretations, justified preprocessing, model metrics, comparisons, cluster evaluation where relevant, citations for retrieved claims, limitations and reproducibility details.

## Responsible use
Do not expose customer-level personal data unnecessarily. Distinguish association from causation. Do not claim code was executed or invent metrics/business outcomes. Human review is required.
