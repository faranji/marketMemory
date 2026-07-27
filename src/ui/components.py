"""Reusable Streamlit components."""
import streamlit as st
def render_disclaimer(text:str)->None:st.caption(text)
def render_confidence_panel(payload:dict)->None:
    # Show label, evidence count, missing-data and abstention reasons; avoid decorative gauges.
    raise NotImplementedError
def render_event_source(payload:dict)->None:
    raise NotImplementedError
