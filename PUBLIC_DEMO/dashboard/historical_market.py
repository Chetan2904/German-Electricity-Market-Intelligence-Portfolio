
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path

DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "german_energy_market_eex_2018_2026.csv"
)

@st.cache_data
def load_historical_data():
    return pd.read_csv(DATA_PATH, parse_dates=["Month"])


def render_historical_market():

    if not DATA_PATH.is_file():
        st.error(
            "Synthetic demonstration dataset is missing. "
            "Check the PUBLIC_DEMO directory."
        )
        return

    data = load_historical_data()

    with st.expander("About this project | Executive Overview"):
        st.markdown(
            """
            **An interactive analytical framework for understanding
            electricity-market dynamics.**

            Explore electricity prices, natural gas costs,
            carbon pricing and renewable generation using Python,
            interactive visualizations and econometric methods.

            **Analytical focus:** Energy security · Electricity
            affordability · Energy transition

            **Demonstration period:** November 2018–October 2026

            **Data:** Fully synthetic observations.
            No displayed results represent actual German market outcomes.
            """
        )

    start_date, end_date = st.date_input(
        "Historical analysis period",
        value=(
            data["Month"].min().date(),
            data["Month"].max().date()
        ),
        min_value=data["Month"].min().date(),
        max_value=data["Month"].max().date(),
        key="historical_date_range"
    )

    filtered = data[
        data["Month"].dt.date.between(
            start_date, end_date
        )
    ]

    if filtered.empty:
        st.warning("No data available for this period.")
        return

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Market Overview",
        "🌱 Energy Transition",
        "📈 Econometrics",
        "📚 Methodology"
    ])

    with tab1:
        st.markdown("### Executive Market Indicators")
        st.caption(
            "Synthetic demonstration data | "
            "Indicators update with the selected analysis period."
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Electricity Price",
            f"€{filtered['Electricity_Price_EUR_MWh'].mean():.2f}/MWh"
        )

        col2.metric(
            "Natural Gas Price",
            f"${filtered['Gas_Price_USD_MMBtu'].mean():.2f}/MMBtu"
        )

        col3.metric(
            "EU ETS Carbon Price",
            f"€{filtered['Carbon_Auction_Price_EUR_tCO2'].mean():.2f}/tCO₂"
        )

        total_load = filtered["Grid_Load_MWh"].sum()
        total_wind_solar = (
            filtered["Wind_Generation_MWh"].sum()
            + filtered["Solar_Generation_MWh"].sum()
        )

        wind_solar_coverage = (
            100 * total_wind_solar / total_load
            if total_load > 0 else float("nan")
        )

        col4.metric(
            "Wind & Solar / Grid Load",
            f"{wind_solar_coverage:.1f}%"
        )

        st.caption(
            "Wind & solar coverage = total wind and solar generation "
            "divided by total grid load for the selected period. "
            "This is not the official renewable electricity share."
        )

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=filtered["Month"],
                y=filtered["Electricity_Price_EUR_MWh"],
                name="Electricity",
                line=dict(color="#38bdf8", width=3)
            )
        )

        fig.add_trace(
            go.Scatter(
                x=filtered["Month"],
                y=filtered["Gas_Price_USD_MMBtu"],
                name="Natural Gas",
                yaxis="y2",
                line=dict(color="#fbbf24", width=3)
            )
        )

        fig.update_layout(
            title="German Electricity and European Natural Gas Prices",
            template="plotly_dark",
            height=500,
            yaxis=dict(title="Electricity (€/MWh)"),
            yaxis2=dict(
                title="Natural Gas (USD/MMBtu)",
                overlaying="y",
                side="right"
            ),
            legend=dict(orientation="h")
        )

        st.plotly_chart(fig, use_container_width=True)

        st.caption(
            "Electricity and natural gas prices are displayed on "
            "separate Y-axes with different units. Their visual "
            "movements should not be interpreted as proportional "
            "price changes or evidence of causation."
        )


        # ========================================================
        # ENERGY CRISIS
        # ========================================================

        st.divider()
        st.subheader(
            f"Illustrative Electricity Price Analysis | "
            f"{filtered['Month'].min():%b %Y} – "
            f"{filtered['Month'].max():%b %Y}"
        )

        st.markdown(
            "This interactive chart demonstrates historical-period analysis "
            "using **synthetic monthly electricity prices**. The 2021–2022 "
            "highlight provides historical context only; the plotted values "
            "are artificially generated and do not represent observed "
            "German electricity-market outcomes."
        )

        crisis_fig = go.Figure()

        crisis_fig.add_trace(
            go.Scatter(
                x=filtered["Month"],
                y=filtered["Electricity_Price_EUR_MWh"],
                name="Electricity Price",
                line=dict(color="#38bdf8", width=3)
            )
        )

        # Highlight the historical European energy-crisis period
        # as context only; the plotted observations are synthetic.
        crisis_fig.add_vrect(
            x0="2021-01-01",
            x1="2022-12-31",
            fillcolor="#f59e0b",
            opacity=0.08,
            line_width=0,
            annotation_text="Historical context: 2021–2022",
            annotation_position="top left"
        )

        crisis_fig.update_layout(
            title="Illustrative Monthly Electricity Prices | Synthetic Data",
            template="plotly_dark",
            height=450,
            yaxis_title="Electricity Price (€/MWh)"
        )

        st.plotly_chart(crisis_fig, use_container_width=True)

        with st.expander("How to interpret this analysis"):
            st.markdown(
                "The chart illustrates how analysts can examine monthly "
                "electricity-price movements and compare selected periods. "
                "A historical event annotation provides context but does "
                "not establish a causal relationship. Because the public "
                "dataset is synthetic, no conclusions about actual German "
                "electricity prices or the effects of the European energy "
                "crisis should be drawn from these observations."
            )


        # ========================================================

    with tab2:
        # RENEWABLE ENERGY TRANSITION
        # ========================================================

        st.subheader("Renewable Energy Transition")

        renewable_fig = go.Figure()

        renewable_fig.add_trace(
            go.Scatter(
                x=filtered["Month"],
                y=filtered["Wind_Generation_MWh"] / 1_000_000,
                name="Wind",
                stackgroup="renewables",
                line=dict(color="#38bdf8")
            )
        )

        renewable_fig.add_trace(
            go.Scatter(
                x=filtered["Month"],
                y=filtered["Solar_Generation_MWh"] / 1_000_000,
                name="Solar",
                stackgroup="renewables",
                line=dict(color="#fbbf24")
            )
        )

        renewable_fig.update_layout(
            title="Monthly Wind and Solar Electricity Generation",
            template="plotly_dark",
            height=450,
            yaxis_title="Generation (TWh)"
        )

        st.plotly_chart(renewable_fig, use_container_width=True)

        # ========================================================
        # FOSSIL ELECTRICITY GENERATION
        # ========================================================

        st.divider()
        st.subheader("Fossil Electricity Generation")

        fossil_fig = go.Figure()

        fossil_sources = {
            "Natural Gas": "Gas_Generation_MWh",
            "Lignite": "Lignite_Generation_MWh",
            "Hard Coal": "Hard_Coal_Generation_MWh"
        }

        for name, column in fossil_sources.items():

            fossil_fig.add_trace(
                go.Scatter(
                    x=filtered["Month"],
                    y=filtered[column] / 1_000_000,
                    name=name,
                    stackgroup="fossil"
                )
            )

        fossil_fig.update_layout(
            title="Monthly Fossil Electricity Generation",
            template="plotly_dark",
            height=450,
            yaxis_title="Generation (TWh)"
        )

        st.plotly_chart(fossil_fig, use_container_width=True)


        # ========================================================

    with tab3:
        # ECONOMETRIC ANALYSIS
        # ========================================================

        st.header("Econometric Market Analysis")

        st.markdown(
            "Statistical relationships between German wholesale "
            "electricity prices, European natural gas prices, "
            "carbon prices and residual electricity demand."
        )

        # Correlation heatmap based on selected months

        correlation_columns = {
            "Electricity_Price_EUR_MWh": "Electricity",
            "Gas_Price_USD_MMBtu": "Natural Gas",
            "Carbon_Auction_Price_EUR_tCO2": "Carbon",
            "Residual_Load_GWh": "Residual Load",
            "Wind_Solar_to_Load_Pct": "Wind + Solar / Load"
        }

        correlation_data = filtered[
            list(correlation_columns.keys())
        ].rename(columns=correlation_columns)

        if len(correlation_data) >= 3:

            correlation_matrix = correlation_data.corr()

            heatmap = go.Figure(
                data=go.Heatmap(
                    z=correlation_matrix.values,
                    x=correlation_matrix.columns,
                    y=correlation_matrix.index,
                    zmin=-1,
                    zmax=1,
                    colorscale="RdBu",
                    reversescale=True,
                    text=correlation_matrix.round(2).values,
                    texttemplate="%{text}",
                    hovertemplate="%{x} vs %{y}: %{z:.3f}<extra></extra>"
                )
            )

            heatmap.update_layout(
                title="Synthetic Energy Market Correlations",
                template="plotly_dark",
                height=480
            )

            st.plotly_chart(heatmap, use_container_width=True)

            st.caption(
                "Correlations are calculated using the selected "
                "historical date range. Correlation does not "
                "establish causation."
            )

        else:
            st.info("Select at least three months to view correlations.")

        # ========================================================
        # SYNTHETIC REGRESSION DEMONSTRATION
        # ========================================================

        st.subheader("Econometric Demonstration | Synthetic Data")

        st.warning(
            "These regression results are calculated exclusively "
            "from artificially generated observations. "
            "They are not empirical findings about Germany."
        )

        import statsmodels.api as sm

        predictors = [
            "Gas_Price_USD_MMBtu",
            "Carbon_Auction_Price_EUR_tCO2",
            "Residual_Load_GWh"
        ]

        model_data = filtered[
            ["Electricity_Price_EUR_MWh"] + predictors
        ].dropna()

        if len(model_data) < 12:
            st.info(
                "Select at least 12 months to display the "
                "illustrative regression. Larger samples are "
                "preferable for statistical interpretation."
            )
        else:
            X = sm.add_constant(
                model_data[predictors],
                has_constant="add"
            )
            y = model_data["Electricity_Price_EUR_MWh"]

            if X.shape[1] != 4 or (
                __import__("numpy").linalg.matrix_rank(X.to_numpy()) < 4
            ):
                st.warning(
                    "Regression cannot be estimated reliably "
                    "because the selected predictors are "
                    "linearly dependent."
                )
            else:
                model = sm.OLS(y, X).fit(
                    cov_type="HAC",
                    cov_kwds={"maxlags": 3}
                )

                regression_results = pd.DataFrame({
                    "Variable": model.params.index,
                    "Coefficient": model.params.values,
                    "HAC p-value": model.pvalues.values,
                    "95% CI Lower": model.conf_int()[0].values,
                    "95% CI Upper": model.conf_int()[1].values
                })

                st.dataframe(
                    regression_results.round(4),
                    use_container_width=True,
                    hide_index=True
                )

                col_a, col_b = st.columns(2)

                with col_a:
                    st.metric(
                        "Synthetic Sample R²",
                        f"{model.rsquared:.3f}"
                    )

                with col_b:
                    st.metric(
                        "Regression Observations",
                        f"{int(model.nobs)}"
                    )

                st.caption(
                    "Illustrative OLS regression with HAC "
                    "standard errors (3 lags). Estimates use "
                    "the selected date range. The data are "
                    "synthetic, and statistical significance "
                    "does not establish causality. HAC inference "
                    "does not resolve potential nonstationarity, "
                    "endogeneity or model misspecification."
                )

        # ========================================================

    with tab4:
        # METHODOLOGY AND RESEARCH LIMITATIONS
        # ========================================================

        st.header("Methodology & Research Limitations")

        st.info(
            "Research integrity: This public dashboard demonstrates "
            "analytical workflows using synthetic data. The separate "
            "empirical research project uses historical market datasets "
            "subject to source-specific licensing and redistribution "
            "requirements. Synthetic regression results must not be "
            "presented as empirical findings."
        )


        with st.expander("Data Sources and Methodology", expanded=False):
            st.markdown("""
        ### Public demonstration dataset

        This dashboard uses 96 artificially generated monthly
        observations covering November 2018–October 2026.

        **No actual historical market observations are included
        in the public demonstration dataset.**

        The synthetic variables represent:
        - Wholesale electricity prices (EUR/MWh).
        - European natural gas prices (USD/MMBtu).
        - Carbon auction prices (EUR/tCO2).
        - Wind and solar generation.
        - Electricity demand and residual load.

        ### Econometric demonstration

        An illustrative ordinary least squares (OLS)
        regression relates synthetic electricity prices
        to synthetic gas prices, carbon prices and
        residual electricity demand.

        Heteroskedasticity and autocorrelation-consistent
        (HAC) standard errors use three monthly lags.

        These estimates demonstrate analytical methods,
        not actual German electricity-market relationships.

        ### Original research project

        The separate research project examines actual
        historical observations obtained from:

        - Bundesnetzagentur SMARD.
        - World Bank Pink Sheet.
        - European Energy Exchange (EEX).

        Original research datasets are not included in
        this public demonstration while relevant
        redistribution permissions are being reviewed.

        ### Limitations

        - All displayed observations are synthetic.
        - Synthetic relationships are imposed by the
          data-generation process.
        - Results cannot support conclusions about
          actual German electricity markets.
        - Statistical associations do not establish causation.
        - The dashboard does not provide real-market forecasts.
        - Wholesale electricity prices differ from
          household retail electricity tariffs.
        """)

        st.caption(
            "Research dashboard developed by Chetan Masram. "
            "Synthetic demonstration for educational and "
            "professional portfolio purposes."
        )
