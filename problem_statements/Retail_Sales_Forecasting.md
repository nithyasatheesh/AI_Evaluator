# Project: AI-Powered Retail Sales Forecasting & Business Intelligence

## Goal
Forecast sales for store-item combinations using historical daily sales to support inventory and replenishment planning, with clear measurement of forecast error and uncertainty.

## Data sources
Use the supplied retail_data.csv and Retail_Forecasting_Education_Text.csv where available, plus approved forecasting-method and responsible-AI reference documents. Validate actual fields, date range, store/item keys and sales units. A missing store-item-date record must not automatically be treated as zero sales unless evidence supports that interpretation.

## Milestone 1 — EDA and baseline forecasting
Parse dates, sort observations chronologically, inspect duplicates/missing dates/values, explore trend, seasonality and store/item variation, create calendar features, establish naive or seasonal-naive baselines and a Linear Regression baseline, and evaluate using a chronological holdout with MAE, RMSE and/or sMAPE.

## Milestone 2 — Machine learning
Build Decision Tree, Random Forest and boosting regressors with lag/rolling/calendar features available at forecast time. Tune using chronological or rolling-origin validation, compare with baselines, inspect residuals and forecast bias, and assess feature importance.

## Milestone 3 — Deep learning
Build a feed-forward or sequence model such as LSTM/GRU, construct sequences in chronological order, fit scaling on training data only, prevent leakage, and compare with ML and naive baselines on the same future holdout and horizon.

## Milestone 4 — Generative AI and agents
Use LLMs to summarize validated actuals and forecast outputs without inventing numbers; implement RAG over approved forecasting documents with citations; enable schema-aware read-only Text-to-SQL; coordinate data querying, retrieval and summarization; test temporal correctness, grounding, SQL safety and prompt injection.

## Expected evidence
Data validation, time-series charts, leakage-aware features, baseline and candidate metrics, validation design, residual analysis, model comparisons, forecast horizon, interpretations and limitations.

## Responsible use
Clearly distinguish historical actuals from forecasts and state the horizon. Do not claim causal effects, savings or inventory improvements unless measured. Do not invent forecast values or claim code was executed.
