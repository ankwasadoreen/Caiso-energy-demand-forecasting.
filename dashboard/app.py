import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(
    page_title="CAISO Energy Demand Forecasting",
    page_icon="⚡",
    layout="wide"
)

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"

HISTORICAL_FILE = DATA_DIR / "caiso_demand_2023_full_year.csv"
FORECAST_FILE = DATA_DIR / "forecast_results.csv"
MODEL_COMPARISON_FILE = DATA_DIR / "model_comparison.csv"
XGBOOST_PREDICTIONS_FILE = DATA_DIR / "xgboost_predictions.csv"
XGBOOST_IMPORTANCE_FILE = DATA_DIR / "xgboost_feature_importance.csv"

st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #1f2937;
        margin-bottom: 5px;
    }
    .subtitle {
        font-size: 17px;
        color: #6b7280;
        margin-bottom: 25px;
    }
    .section-title {
        font-size: 27px;
        font-weight: 700;
        color: #1f2937;
        margin-top: 25px;
        margin-bottom: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def load_csv(path, required=True):
    if path.exists():
        return pd.read_csv(path)
    if required:
        st.error(f"Required file not found: {path.name}")
        st.stop()
    return None

def calculate_mae(actual, predicted):
    return (actual - predicted).abs().mean()

def calculate_rmse(actual, predicted):
    return (((actual - predicted) ** 2).mean()) ** 0.5

def calculate_mape(actual, predicted):
    valid = actual != 0
    return (((actual[valid] - predicted[valid]).abs() / actual[valid]).mean() * 100)

historical_df = load_csv(HISTORICAL_FILE)
forecast_df = load_csv(FORECAST_FILE)
model_comparison = load_csv(MODEL_COMPARISON_FILE, required=False)
xgb_predictions = load_csv(XGBOOST_PREDICTIONS_FILE, required=False)
xgb_importance = load_csv(XGBOOST_IMPORTANCE_FILE, required=False)

historical_df["datetime"] = pd.to_datetime(historical_df["datetime"])
forecast_df["datetime"] = pd.to_datetime(forecast_df["datetime"])

if xgb_predictions is not None and "datetime" in xgb_predictions.columns:
    xgb_predictions["datetime"] = pd.to_datetime(xgb_predictions["datetime"])

actual = forecast_df["Actual Demand"]

statistical_metrics = pd.DataFrame({
    "Model": ["SARIMA", "Prophet", "Hybrid (SARIMA + Prophet)"],
    "MAE (MWh)": [
        calculate_mae(actual, forecast_df["SARIMA Forecast"]),
        calculate_mae(actual, forecast_df["Prophet Forecast"]),
        calculate_mae(actual, forecast_df["Hybrid Forecast"])
    ],
    "RMSE (MWh)": [
        calculate_rmse(actual, forecast_df["SARIMA Forecast"]),
        calculate_rmse(actual, forecast_df["Prophet Forecast"]),
        calculate_rmse(actual, forecast_df["Hybrid Forecast"])
    ],
    "MAPE (%)": [
        calculate_mape(actual, forecast_df["SARIMA Forecast"]),
        calculate_mape(actual, forecast_df["Prophet Forecast"]),
        calculate_mape(actual, forecast_df["Hybrid Forecast"])
    ]
}).round(2)

if model_comparison is None:
    model_comparison = pd.DataFrame({
        "Model": [
            "SARIMA",
            "Prophet",
            "Hybrid (SARIMA + Prophet)",
            "Weather-only Random Forest",
            "Enhanced Random Forest",
            "XGBoost"
        ],
        "MAE (MWh)": [1214.92, 3047.00, 1261.45, 1939.99, 398.17, 354.48],
        "RMSE (MWh)": [1604.52, 3728.00, 1545.61, 2403.55, 526.51, 461.88],
        "MAPE (%)": [5.25, 13.05, 5.35, None, 1.67, 1.50],
        "R²": [None, None, None, 0.0186, 0.9475, 0.9596]
    })

st.markdown(
    '<div class="main-title">⚡ Energy Demand Forecasting Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    CAISO hourly electricity-demand forecasting using statistical
    time-series models, NOAA weather data, Random Forest, and XGBoost
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.header("Dashboard Controls")
region = st.sidebar.selectbox("Select Region", ["CAISO"])
statistical_model = st.sidebar.selectbox(
    "Statistical Forecast Model",
    ["All Models", "SARIMA", "Prophet", "Hybrid"]
)
dashboard_section = st.sidebar.radio(
    "Dashboard Section",
    [
        "Project Overview",
        "Historical Demand",
        "Statistical Forecasts",
        "Weather and Machine Learning",
        "Final Model Comparison",
        "Feature Importance",
        "Conclusions and Downloads"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    """
    This project compares statistical and machine-learning
    approaches for hourly CAISO electricity-demand forecasting.
    """
)

if dashboard_section == "Project Overview":
    st.markdown('<div class="section-title">Project Overview</div>', unsafe_allow_html=True)
    st.write(
        """
        This project evaluates multiple approaches for forecasting
        hourly California electricity demand.

        **Phase 1** developed SARIMA, Prophet, and Hybrid forecasting
        models using historical CAISO demand.

        **Phase 2** integrated NOAA weather observations and developed
        Weather-only Random Forest, Enhanced Random Forest, and XGBoost
        models using weather, temporal, lagged-demand, and rolling-average
        features.
        """
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Best Overall Model", "XGBoost")
    col2.metric("Lowest MAE", "354.48 MWh")
    col3.metric("Lowest MAPE", "1.50%")
    col4.metric("Highest R²", "0.9596")

    st.markdown('<div class="section-title">Main Result</div>', unsafe_allow_html=True)
    st.success(
        """
        XGBoost achieved the strongest overall forecasting performance,
        with MAE 354.48 MWh, RMSE 461.88 MWh, MAPE 1.50%, and R² 0.9596.
        """
    )

    st.markdown('<div class="section-title">Model Summary</div>', unsafe_allow_html=True)
    st.dataframe(model_comparison, use_container_width=True, hide_index=True)

    st.markdown('<div class="section-title">Project Workflow</div>', unsafe_allow_html=True)
    st.code(
        """
        CAISO Electricity Demand
                  +
           NOAA Weather Data
                  |
                  v
        Data Cleaning & Integration
                  |
                  v
        Exploratory Data Analysis
                  |
                  v
          Feature Engineering
       (Time, Lag, Rolling, Weather)
                  |
          +-------+-------+
          |               |
          v               v
    Statistical Models    Machine Learning
    SARIMA                Random Forest
    Prophet               Enhanced RF
    Hybrid                XGBoost
          |               |
          +-------+-------+
                  |
                  v
          Model Evaluation
        MAE | RMSE | MAPE | R²
                  |
                  v
         Best Model: XGBoost
                  |
                  v
         Streamlit Dashboard
                  +
       Automated Commentary
        """
    )

elif dashboard_section == "Historical Demand":
    st.markdown('<div class="section-title">Historical CAISO Electricity Demand</div>', unsafe_allow_html=True)

    fig_hist, ax_hist = plt.subplots(figsize=(14, 5))
    ax_hist.plot(historical_df["datetime"], historical_df["demand_mwh"], linewidth=1)
    ax_hist.set_title(f"{region} Hourly Electricity Demand — 2023")
    ax_hist.set_xlabel("Date")
    ax_hist.set_ylabel("Demand (MWh)")
    ax_hist.grid(alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig_hist)
    plt.close(fig_hist)

    col1, col2, col3 = st.columns(3)
    col1.metric("Observations", f"{len(historical_df):,}")
    col2.metric("Average Demand", f'{historical_df["demand_mwh"].mean():,.0f} MWh')
    col3.metric("Peak Demand", f'{historical_df["demand_mwh"].max():,.0f} MWh')

    st.info(
        """
        Historical CAISO electricity demand shows strong hourly,
        daily, weekly, and seasonal patterns, with higher demand
        during California's summer months.
        """
    )

elif dashboard_section == "Statistical Forecasts":
    st.markdown('<div class="section-title">Statistical Forecasting Models</div>', unsafe_allow_html=True)

    fig_forecast, ax_forecast = plt.subplots(figsize=(14, 6))
    ax_forecast.plot(
        forecast_df["datetime"],
        forecast_df["Actual Demand"],
        label="Actual Demand",
        linewidth=2
    )

    if statistical_model in ["SARIMA", "All Models"]:
        ax_forecast.plot(
            forecast_df["datetime"],
            forecast_df["SARIMA Forecast"],
            linestyle="--",
            label="SARIMA"
        )

    if statistical_model in ["Prophet", "All Models"]:
        ax_forecast.plot(
            forecast_df["datetime"],
            forecast_df["Prophet Forecast"],
            linestyle=":",
            label="Prophet"
        )

    if statistical_model in ["Hybrid", "All Models"]:
        ax_forecast.plot(
            forecast_df["datetime"],
            forecast_df["Hybrid Forecast"],
            label="Hybrid"
        )

    ax_forecast.set_title("Actual vs Forecasted CAISO Electricity Demand")
    ax_forecast.set_xlabel("Date")
    ax_forecast.set_ylabel("Demand (MWh)")
    ax_forecast.legend()
    ax_forecast.grid(alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig_forecast)
    plt.close(fig_forecast)

    st.markdown('<div class="section-title">Statistical Model Performance</div>', unsafe_allow_html=True)
    st.dataframe(statistical_metrics, use_container_width=True, hide_index=True)
    st.info(
        """
        SARIMA achieved the strongest average forecasting accuracy
        among the statistical models, while the Hybrid model achieved
        the lowest RMSE.
        """
    )

elif dashboard_section == "Weather and Machine Learning":
    st.markdown('<div class="section-title">NOAA Weather Integration</div>', unsafe_allow_html=True)

    st.write(
        """
        NOAA hourly weather observations were integrated from:

        - San Francisco
        - Los Angeles
        - Sacramento
        - Fresno
        - San Diego

        Weather variables included temperature, humidity, wind speed,
        atmospheric pressure, and precipitation.
        """
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Integrated Observations", "8,760")
    col2.metric("Integrated Variables", "34")
    col3.metric("Remaining Missing Values", "0")

    st.markdown('<div class="section-title">Feature Engineering</div>', unsafe_allow_html=True)
    st.write(
        """
        Enhanced models included:

        - Hour
        - Day of week
        - Month
        - Quarter
        - Day of year
        - Weekend indicator
        - Demand lag 1 hour
        - Demand lag 24 hours
        - Demand lag 168 hours
        - Rolling mean 24 hours
        - Rolling mean 168 hours
        - Temperature
        - Humidity
        - Wind speed
        - Pressure
        - Precipitation
        """
    )

    st.markdown('<div class="section-title">Machine-Learning Results</div>', unsafe_allow_html=True)

    machine_learning_results = model_comparison[
        model_comparison["Model"].isin(
            [
                "Weather-only Random Forest",
                "Enhanced Random Forest",
                "XGBoost"
            ]
        )
    ]

    st.dataframe(machine_learning_results, use_container_width=True, hide_index=True)

    st.warning(
        """
        Weather alone produced limited predictive accuracy.
        Performance improved substantially after temporal,
        lagged-demand, and rolling-average features were added.
        """
    )

    if xgb_predictions is not None:
        required_columns = {"datetime", "actual_demand", "xgboost_prediction"}

        if required_columns.issubset(xgb_predictions.columns):
            st.markdown('<div class="section-title">XGBoost: Actual vs Predicted Demand</div>', unsafe_allow_html=True)

            fig_xgb, ax_xgb = plt.subplots(figsize=(14, 6))
            ax_xgb.plot(
                xgb_predictions["datetime"],
                xgb_predictions["actual_demand"],
                label="Actual Demand",
                linewidth=1.5
            )
            ax_xgb.plot(
                xgb_predictions["datetime"],
                xgb_predictions["xgboost_prediction"],
                label="XGBoost Prediction",
                linewidth=1
            )
            ax_xgb.set_title("XGBoost Actual vs Predicted Demand")
            ax_xgb.set_xlabel("Datetime")
            ax_xgb.set_ylabel("Demand (MWh)")
            ax_xgb.legend()
            ax_xgb.grid(alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig_xgb)
            plt.close(fig_xgb)
        else:
            st.warning("XGBoost predictions file exists, but expected columns were not found.")
    else:
        st.info("XGBoost prediction file is unavailable.")

elif dashboard_section == "Final Model Comparison":
    st.markdown('<div class="section-title">Final Model Performance Comparison</div>', unsafe_allow_html=True)
    st.dataframe(model_comparison, use_container_width=True, hide_index=True)

    fig_mae, ax_mae = plt.subplots(figsize=(11, 5))
    ax_mae.bar(model_comparison["Model"], model_comparison["MAE (MWh)"])
    ax_mae.set_title("Model Comparison by MAE")
    ax_mae.set_ylabel("MAE (MWh)")
    ax_mae.tick_params(axis="x", rotation=25)
    ax_mae.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig_mae)
    plt.close(fig_mae)

    fig_rmse, ax_rmse = plt.subplots(figsize=(11, 5))
    ax_rmse.bar(model_comparison["Model"], model_comparison["RMSE (MWh)"])
    ax_rmse.set_title("Model Comparison by RMSE")
    ax_rmse.set_ylabel("RMSE (MWh)")
    ax_rmse.tick_params(axis="x", rotation=25)
    ax_rmse.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig_rmse)
    plt.close(fig_rmse)

    mape_df = model_comparison.dropna(subset=["MAPE (%)"])
    fig_mape, ax_mape = plt.subplots(figsize=(11, 5))
    ax_mape.bar(mape_df["Model"], mape_df["MAPE (%)"])
    ax_mape.set_title("Model Comparison by MAPE")
    ax_mape.set_ylabel("MAPE (%)")
    ax_mape.tick_params(axis="x", rotation=25)
    ax_mape.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig_mape)
    plt.close(fig_mape)

    st.success(
        """
        XGBoost achieved the lowest MAE, RMSE, and MAPE.
        Enhanced Random Forest ranked second, while SARIMA
        remained the strongest statistical model.
        """
    )

elif dashboard_section == "Feature Importance":
    st.markdown('<div class="section-title">XGBoost Feature Importance</div>', unsafe_allow_html=True)

    if xgb_importance is None:
        st.warning("xgboost_feature_importance.csv was not found in the data/processed folder.")
    else:
        required_columns = {"Feature", "Importance"}

        if required_columns.issubset(xgb_importance.columns):
            top_features = (
                xgb_importance
                .sort_values("Importance", ascending=False)
                .head(15)
            )

            st.dataframe(top_features, use_container_width=True, hide_index=True)

            plot_features = top_features.sort_values("Importance", ascending=True)

            fig_imp, ax_imp = plt.subplots(figsize=(10, 7))
            ax_imp.barh(plot_features["Feature"], plot_features["Importance"])
            ax_imp.set_title("Top 15 XGBoost Feature Importances")
            ax_imp.set_xlabel("Importance")
            ax_imp.set_ylabel("Feature")
            plt.tight_layout()
            st.pyplot(fig_imp)
            plt.close(fig_imp)
        else:
            st.error(
                "Feature importance file exists but does not contain Feature and Importance columns."
            )

elif dashboard_section == "Conclusions and Downloads":
    st.markdown('<div class="section-title">Final Project Conclusion</div>', unsafe_allow_html=True)

    st.write(
        """
        XGBoost achieved the strongest overall forecasting performance
        with:

        - MAE: **354.48 MWh**
        - RMSE: **461.88 MWh**
        - MAPE: **1.50%**
        - R²: **0.9596**

        Historical-demand lag features were the strongest predictors,
        while weather variables provided complementary information.
        """
    )

    st.markdown('<div class="section-title">Automated Forecast Commentary</div>', unsafe_allow_html=True)

    st.caption(
        """
        This prototype uses pre-generated natural-language commentary
        and does not require a paid external API.
        """
    )

    commentary = """
    CAISO electricity demand follows strong hourly, daily, weekly,
    and seasonal patterns.

    Historical electricity demand is the dominant predictor of
    near-term consumption, especially demand from the previous hour
    and demand from the same hour on the previous day.

    XGBoost achieved the strongest overall forecasting performance,
    with an MAE of 354.48 MWh, RMSE of 461.88 MWh, MAPE of 1.50%,
    and R² of 0.9596.

    Weather information alone produced limited predictive accuracy.
    Performance improved substantially after temporal variables,
    lagged demand, and rolling averages were incorporated.

    Future improvements could include multiple years of CAISO demand,
    renewable generation, electricity prices, holidays, extreme
    weather events, and real-time weather observations.
    """

    st.info(commentary)

    st.markdown('<div class="section-title">Download Results</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button(
            label="Download Model Comparison",
            data=model_comparison.to_csv(index=False),
            file_name="model_comparison.csv",
            mime="text/csv"
        )

    with col2:
        st.download_button(
            label="Download Statistical Forecasts",
            data=forecast_df.to_csv(index=False),
            file_name="forecast_results.csv",
            mime="text/csv"
        )

    with col3:
        if xgb_predictions is not None:
            st.download_button(
                label="Download XGBoost Predictions",
                data=xgb_predictions.to_csv(index=False),
                file_name="xgboost_predictions.csv",
                mime="text/csv"
            )
        else:
            st.info("XGBoost prediction file unavailable.")
