import streamlit as st
from historical_market import render_historical_market

st.set_page_config(
    page_title="German Electricity Market Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.block-container {
    padding-top: 4rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}
.portfolio-eyebrow {
    color: #38bdf8;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
.portfolio-title {
    font-size: clamp(2rem, 4vw, 3.4rem);
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 1.15;
    margin: 0.6rem 0;
}
.portfolio-subtitle {
    color: #a8b5c7;
    font-size: 1.1rem;
    margin-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="portfolio-eyebrow">'
    'ENERGY MARKET ANALYTICS · PROFESSIONAL PORTFOLIO'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="portfolio-title">'
    'German Electricity Market Intelligence'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="portfolio-subtitle">'
    'Wholesale Electricity Markets · Renewable Generation · '
    'Econometric Analysis | 2018–2026'
    '</div>',
    unsafe_allow_html=True
)

st.warning(
    "SYNTHETIC DATA DEMONSTRATION — All displayed market "
    "observations are artificially generated. "
    "They do not represent actual German electricity-market conditions."
)

st.divider()


st.caption(
    "ANALYTICAL PORTFOLIO | Python · Pandas · Plotly · "
    "Statsmodels · Streamlit"
)

st.markdown(
    "An interactive demonstration of electricity-market analysis, "
    "renewable and conventional generation trends, market-price "
    "relationships, and econometric modelling. "
    "Designed to demonstrate practical analytical workflows "
    "relevant to European energy-market analyst roles."
)

render_historical_market()
