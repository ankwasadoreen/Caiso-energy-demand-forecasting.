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

The enhanced Random Forest was the second-best machine-learning model. SARIMA remained the strongest traditional statistical model.

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
energy_forecasting_llm/
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
01_energy_data_exploration.ipynb
02_noaa_weather_integration.ipynb
03_statistical_forecasting.ipynb
04_random_forest_models.ipynb
05_xgboost_model.ipynb
06_model_comparison.ipynb
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
