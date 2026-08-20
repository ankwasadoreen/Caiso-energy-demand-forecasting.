# CAISO Energy Demand Forecasting Dashboard

A forecasting project that compares statistical time-series models and machine-learning approaches for hourly California electricity demand.

## Project Overview

This project uses CAISO hourly electricity demand and NOAA weather observations to compare:

- SARIMA
- Prophet
- Hybrid SARIMA + Prophet
- Weather-only Random Forest
- Enhanced Random Forest
- XGBoost

The dashboard is built with Streamlit.

## Best Model

XGBoost achieved the strongest overall performance:

| Metric | XGBoost |
|---|---:|
| MAE | 354.48 MWh |
| RMSE | 461.88 MWh |
| MAPE | 1.50% |
| R² | 0.9596 |

The Enhanced Random Forest was the second-best machine-learning model. SARIMA was the strongest statistical forecasting model in Phase 1, while XGBoost achieved the strongest overall performance after weather integration and enhanced feature engineering in Phase 2.

## Project Notebooks

The project is organized into two main analytical notebooks representing two phases of the forecasting workflow.

### Notebook 01 — Energy Demand Exploration & Statistical Forecasting

This notebook focuses on exploratory analysis of CAISO hourly electricity-demand data and the development of traditional time-series forecasting models. The models evaluated include SARIMA, Prophet, and a Hybrid SARIMA–Prophet approach.

Among the Phase 1 statistical forecasting models, SARIMA achieved the best overall accuracy with a MAPE of 5.25%. The Hybrid model provided competitive performance and helped reduce larger forecasting errors, while Prophet was useful for capturing broader trend and seasonal patterns.

### Notebook 02 — NOAA Weather Integration & Machine Learning

This notebook extends the forecasting framework by integrating weather information and applying machine-learning methods. It includes weather-data integration, time-based feature engineering, demand lag features, rolling demand statistics, and machine-learning model development.

The Enhanced Random Forest substantially improved forecasting performance, achieving:

- MAE: 398.17 MW
- RMSE: 526.51 MW
- MAPE: 1.67%
- R²: 0.9475

XGBoost produced the strongest overall Phase 2 performance, achieving:

- MAE: 354.48 MW
- RMSE: 461.88 MW
- MAPE: 1.50%
- R²: 0.9596

Therefore, SARIMA was the strongest model during the statistical forecasting phase, while XGBoost became the best-performing model after weather integration and enhanced feature engineering.


## Feature Engineering

The enhanced machine-learning models use:

- Hour of day
- Day of week
- Month
- Quarter
- Day of year
- Weekend indicator
- Demand lag 1 hour
- Demand lag 24 hours
- Demand lag 168 hours
- 24-hour rolling mean
- 168-hour rolling mean
- Temperature
- Humidity
- Wind speed
- Atmospheric pressure
- Precipitation

## Repository Structure

```text
Caiso_energy_demand_ forecasting/
├── dashboard/
│   └── app.py
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── outputs/
│   ├── figures/
│   └── tables/
├── docs/
├── .gitignore
├── requirements.txt
└── README.md
```

## Expected Processed Data Files

Place these files in `data/processed/`:

```text
caiso_demand_2023_full_year.csv
forecast_results.csv
model_comparison.csv
xgboost_predictions.csv
xgboost_feature_importance.csv
```

## Suggested Notebook Naming

Keep notebooks in execution order:

```text
## Notebook Organization

The analysis is organized into two main notebooks, corresponding to the two phases of the project:

1. `01_energy_data_exploration. ipynb`  
   Energy-demand exploration and statistical forecasting using SARIMA, Prophet, and the Hybrid forecasting approach.

2. `02_noaa_weather_integration. ipynb`  
   NOAA weather integration, feature engineering, Enhanced Random Forest, XGBoost, and final machine-learning model evaluation.

The notebooks are numbered in execution order to provide a clear progression from statistical forecasting to weather-enhanced machine-learning forecasting.
```

Rename your existing notebooks to match these names where appropriate rather than creating duplicate analyses.

## Run Locally

Create a virtual environment if desired, then install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit dashboard from the repository root:

```bash
python -m streamlit run dashboard/app.py
```

The app will normally open at:

```text
http://localhost:8501
```

## Automated Commentary

The dashboard includes pre-generated natural-language forecasting commentary. The current prototype does not require a paid external LLM API.

The architecture is designed so a live LLM component can be added later if desired.

## Data Notes

Raw and processed energy/weather datasets can be large. Before uploading files to GitHub, confirm that:

- the data source permits redistribution;
- no file exceeds GitHub size limits;
- only files necessary to reproduce the analysis are committed.

For large or redistributable public datasets, it is often better to document the source and provide a download script rather than commit the full raw files.

## Future Improvements

Potential extensions include:

- Multiple years of CAISO demand
- Renewable generation variables
- Electricity prices
- Holiday indicators
- Extreme-weather indicators
- Real-time weather feeds
- Hyperparameter optimization
- Time-aware cross-validation
- Live model serving
- Optional live LLM commentary

## Portfolio Summary

This project demonstrates an end-to-end data-science workflow covering:

- Time-series analysis
- Weather-data integration
- Feature engineering
- Statistical forecasting
- Ensemble forecasting
- Random Forest
- XGBoost
- Model evaluation
- Explainability through feature importance
- Streamlit dashboard development
- Natural-language interpretation of model results
