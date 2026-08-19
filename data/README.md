# Data Folder

Use this structure:

```text
data/
├── raw/
└── processed/
```

## raw/

Place original source files here when redistribution is permitted.

Examples:
- Original CAISO demand export
- Original NOAA weather exports

Do not modify raw files manually.

## processed/

Place cleaned and model-ready files here.

The Streamlit dashboard expects:

- `caiso_demand_2023_full_year.csv`
- `forecast_results.csv`
- `model_comparison.csv`
- `xgboost_predictions.csv`
- `xgboost_feature_importance.csv`

If your existing files currently live directly under `data/`, move them into `data/processed/` or change `DATA_DIR` in `dashboard/app.py`.
