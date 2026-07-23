from __future__ import annotations

import streamlit as st

st.set_page_config(
    page_title="Market Memory",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

dashboard = st.Page("pages/dashboard.py", title="Market Terminal", icon="📈", default=True)
quality = st.Page("pages/data_quality.py", title="Data Quality", icon="🧪")
methodology = st.Page("pages/methodology.py", title="Methodology", icon="🧠")

navigation = st.navigation(
    {
        "Terminal": [dashboard],
        "Research": [quality, methodology],
    }
)
navigation.run()
