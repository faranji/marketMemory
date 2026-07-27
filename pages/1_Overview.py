# Overview: What data is available and is the system healthy?
import streamlit as st
from src.ui.copy import DISCLAIMER
st.title('Market Overview')
st.caption('Historical event context for TUPRS and Borsa İstanbul.')
# TODO: load reviewed events/prices/quality through src.ui.queries.
# Show real coverage; never invent A+ quality or real-time labels.
st.info('Connect this page to Supabase after the pilot pipeline is complete.')
st.caption(DISCLAIMER)
