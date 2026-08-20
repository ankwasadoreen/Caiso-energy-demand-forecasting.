# Notebooks.

This project is organized into two main analytical notebooks representing the two phases of the forecasting workflow.

## 1. Energy Demand Exploration & Statistical Forecasting

`01_energy_data_exploration. ipynb`

This notebook contains the exploration of CAISO hourly electricity-demand data and the statistical forecasting phase. Models evaluated include SARIMA, Prophet, and a Hybrid SARIMA–Prophet model.

SARIMA achieved the strongest overall performance among the Phase 1 statistical models, with a MAPE of 5.25%.

## 2. NOAA Weather Integration & Machine Learning

`02_noaa_weather_integration. ipynb`

This notebook extends the forecasting analysis by integrating NOAA weather data and engineering time-based, lag, and rolling-demand features.

Machine-learning models include the Weather-Only Random Forest, Enhanced Random Forest, and XGBoost.

The Enhanced Random Forest achieved:

- MAE: 398.17 MW
- RMSE: 526.51 MW
- MAPE: 1.67%
- R²: 0.9475

XGBoost achieved the strongest overall Phase 2 performance:

- MAE: 354.48 MW
- RMSE: 461.88 MW
- MAPE: 1.50%
- R²: 0.9596

Therefore, SARIMA was the strongest statistical forecasting model in Phase 1, while XGBoost achieved the best overall forecasting performance after weather integration and enhanced feature engineering in Phase 2.
